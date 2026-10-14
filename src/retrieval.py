# Hybrid Retrieval Pipeline:
# 1. FAISS Dense Vector Search (Sentence Transformers)
# 2. BM25 Sparse Keyword Search
# 3. Hybrid Fusion with Reciprocal Rank Fusion (RRF) / Normalized Weighted Scoring
# 4. Semantic Cross-Encoder / Bi-Encoder Re-Ranking

import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import numpy as np
import faiss
import re
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

class VectorSearchEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Lightweight sentence transformer embedding engine and FAISS index."""
        self.model_name = model_name
        try:
            self.encoder = SentenceTransformer(model_name, local_files_only=True)
        except Exception:
            self.encoder = SentenceTransformer(model_name)
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        self.index = None
        self.chunks = []

    def build_index(self, chunks: List[Dict[str, Any]]):
        """Index all chunk contents using FAISS Flat L2 or Inner Product with normalized embeddings."""
        self.chunks = chunks
        texts = [c["content"] for c in chunks]
        embeddings = self.encoder.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Normalize for cosine similarity via inner product
        faiss.normalize_L2(embeddings)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings.astype(np.float32))

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Dense semantic search returning scored chunks."""
        if self.index is None or len(self.chunks) == 0:
            return []
        q_emb = self.encoder.encode([query], convert_to_numpy=True, show_progress_bar=False)
        faiss.normalize_L2(q_emb)
        scores, indices = self.index.search(q_emb.astype(np.float32), min(top_k, len(self.chunks)))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                chunk = dict(self.chunks[idx])
                chunk["vector_score"] = float(score)
                results.append(chunk)
        return results


class KeywordSearchEngine:
    def __init__(self):
        """BM25 Okapi lexical search engine."""
        self.bm25 = None
        self.chunks = []

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Simple alphanumeric tokenizer with lowercase normalization."""
        return re.findall(r'\b[a-zA-Z0-9_-]+\b', text.lower())

    def build_index(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        corpus = [self.tokenize(c["content"]) for c in chunks]
        self.bm25 = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Sparse BM25 search returning scored chunks."""
        if self.bm25 is None or len(self.chunks) == 0:
            return []
        tokenized_query = self.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        top_indices = np.argsort(scores)[::-1][:min(top_k, len(self.chunks))]
        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score > 0: # Only return non-zero lexical matches
                chunk = dict(self.chunks[idx])
                chunk["bm25_score"] = score
                results.append(chunk)
        return results


class HybridRetrievalPipeline:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.vector_engine = VectorSearchEngine(model_name)
        self.keyword_engine = KeywordSearchEngine()
        self.chunks = []

    def initialize(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.vector_engine.build_index(chunks)
        self.keyword_engine.build_index(chunks)

    def retrieve_hybrid(self, query: str, top_k: int = 6, vector_weight: float = 0.6, bm25_weight: float = 0.4) -> List[Dict[str, Any]]:
        """
        Executes both Vector and Keyword retrieval, fuses scores using min-max normalization,
        and eliminates duplicates.
        """
        vec_results = self.vector_engine.search(query, top_k=top_k * 2)
        kw_results = self.keyword_engine.search(query, top_k=top_k * 2)

        # Normalize vector scores (cosine similarity range [-1, 1], usually [0.2, 0.9])
        v_scores = [r["vector_score"] for r in vec_results]
        v_min, v_max = (min(v_scores), max(v_scores)) if v_scores else (0, 1)

        # Normalize BM25 scores
        k_scores = [r["bm25_score"] for r in kw_results]
        k_min, k_max = (min(k_scores), max(k_scores)) if k_scores else (0, 1)

        fused = {}

        for item in vec_results:
            cid = item["chunk_id"]
            norm_v = (item["vector_score"] - v_min) / (v_max - v_min + 1e-6) if v_max > v_min else 0.8
            fused[cid] = {
                "chunk": item,
                "norm_vector": norm_v,
                "norm_bm25": 0.0,
                "raw_vector": item["vector_score"],
                "raw_bm25": 0.0,
                "retrieval_source": "Vector (FAISS)"
            }

        for item in kw_results:
            cid = item["chunk_id"]
            norm_k = (item["bm25_score"] - k_min) / (k_max - k_min + 1e-6) if k_max > k_min else 0.8
            if cid in fused:
                fused[cid]["norm_bm25"] = norm_k
                fused[cid]["raw_bm25"] = item["bm25_score"]
                fused[cid]["retrieval_source"] = "Hybrid (Vector + BM25)"
            else:
                fused[cid] = {
                    "chunk": item,
                    "norm_vector": 0.0,
                    "norm_bm25": norm_k,
                    "raw_vector": 0.0,
                    "raw_bm25": item["bm25_score"],
                    "retrieval_source": "Keyword (BM25)"
                }

        # Calculate combined hybrid score
        hybrid_candidates = []
        for cid, data in fused.items():
            combined_score = (vector_weight * data["norm_vector"]) + (bm25_weight * data["norm_bm25"])
            chunk_copy = dict(data["chunk"])
            chunk_copy["hybrid_score"] = round(combined_score, 4)
            chunk_copy["retrieval_source"] = data["retrieval_source"]
            chunk_copy["raw_vector"] = round(data["raw_vector"], 4)
            chunk_copy["raw_bm25"] = round(data["raw_bm25"], 4)
            hybrid_candidates.append(chunk_copy)

        hybrid_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return hybrid_candidates[:top_k]

    def semantic_rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic re-ranking step:
        Uses fine-grained cosine similarity between query and candidate chunks to produce
        the final ranked evidence set.
        """
        if not candidates:
            return []

        query_emb = self.vector_engine.encoder.encode([query], convert_to_numpy=True, show_progress_bar=False)
        cand_texts = [f"{c['title']} - {c['content']}" for c in candidates]
        cand_embs = self.vector_engine.encoder.encode(cand_texts, convert_to_numpy=True, show_progress_bar=False)
        
        faiss.normalize_L2(query_emb)
        faiss.normalize_L2(cand_embs)

        rerank_scores = np.dot(cand_embs, query_emb.T).flatten()

        reranked = []
        for i, score in enumerate(rerank_scores):
            item = dict(candidates[i])
            item["rerank_score"] = round(float(score), 4)
            reranked.append(item)

        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_n]
