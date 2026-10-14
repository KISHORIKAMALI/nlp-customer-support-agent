# Document processing, chunking, and embedding generation
import re
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """Clean whitespace and standardize text."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_document(doc: Dict[str, Any], chunk_size: int = 350, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Split a document into semantic chunks with metadata preserved.
    """
    content = clean_text(doc["content"])
    sentences = re.split(r'(?<=[.!?]) +', content)
    
    chunks = []
    current_chunk = []
    current_length = 0
    chunk_index = 0

    for sent in sentences:
        sent_len = len(sent)
        if current_length + sent_len > chunk_size and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "chunk_id": f"{doc['id']}_c{chunk_index}",
                "doc_id": doc["id"],
                "title": doc["title"],
                "category": doc["category"],
                "source": doc["source"],
                "content": chunk_text
            })
            chunk_index += 1
            # overlap handling
            if len(current_chunk) > 1:
                current_chunk = [current_chunk[-1], sent]
                current_length = len(current_chunk[0]) + sent_len
            else:
                current_chunk = [sent]
                current_length = sent_len
        else:
            current_chunk.append(sent)
            current_length += sent_len

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "chunk_id": f"{doc['id']}_c{chunk_index}",
            "doc_id": doc["id"],
            "title": doc["title"],
            "category": doc["category"],
            "source": doc["source"],
            "content": chunk_text
        })

    return chunks

def process_all_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean and chunk all documents in knowledge base."""
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
    return all_chunks
