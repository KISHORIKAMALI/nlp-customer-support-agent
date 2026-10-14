# Command Line Verification and Test Suite
# Tests all 6 Mandatory Demo Questions and the Evaluation Benchmark

import sys
import os
import json

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from knowledge_base.documents import DOCUMENTS
from src.document_processor import process_all_documents
from src.retrieval import HybridRetrievalPipeline
from src.agent_engine import SupportAgentEngine
from src.evaluation import evaluate_pipeline

def run_tests():
    print("=" * 80)
    print("INITIALIZING AGENTIC RAG SYSTEM FOR TESTING")
    print("=" * 80)

    # 1. Process documents
    print("[1/4] Processing and chunking knowledge base documents...")
    chunks = process_all_documents(DOCUMENTS)
    print(f"      Total documents: {len(DOCUMENTS)} -> Total chunks generated: {len(chunks)}")

    # 2. Build retrieval index
    print("[2/4] Initializing FAISS Vector Store and BM25 Lexical Index...")
    retrieval_pipeline = HybridRetrievalPipeline()
    retrieval_pipeline.initialize(chunks)
    print("      Vector embeddings and BM25 index built successfully!")

    # 3. Instantiate Agent Engine
    print("[3/4] Initializing Multi-Agent Engine (Planner, Tools, Verifier)...")
    engine = SupportAgentEngine(retrieval_pipeline)
    print("      Engine ready!\n")

    # 4. Run Mandatory Demo Questions
    demo_questions = [
        "Can I return a damaged laptop?",
        "My order is ORD1001. Where is it?",
        "My order has not arrived. Can I cancel it and get a refund?",
        "Why was my refund rejected?",
        "I want to speak to a human.",
        "How long will the refund take?"
    ]

    print("=" * 80)
    print("EXECUTING MANDATORY DEMO QUESTIONS")
    print("=" * 80)

    conversation_history = []

    for i, q in enumerate(demo_questions, 1):
        print(f"\n--- [DEMO QUESTION {i}] ---")
        print(f"USER: {q}")
        
        # Pass conversation history (especially for follow-up question 6)
        res = engine.process_query(q, conversation_history=conversation_history)
        
        # Record into history
        conversation_history.append({"role": "user", "content": q})
        conversation_history.append({"role": "assistant", "content": res["final_response"]})

        print(f"INTENT: {res['intent']} (Confidence: {res['confidence']})")
        print(f"PLAN: {json.dumps(res['plan'], indent=2)}")
        print(f"RETRIEVAL SOURCES: {res['retrieval_sources']}")
        print(f"TOOLS CALLED: {list(res['tools_called'].keys()) if res['tools_called'] else 'None'}")
        print(f"VERIFICATION: {res['verification']['status']} (Confidence: {res['verification']['confidence_score']})")
        print(f"LATENCY: {res['latency_seconds']}s")
        print(f"FINAL RESPONSE:\n{res['final_response']}")
        print("-" * 60)

    # 5. Run Evaluation Suite
    print("\n" + "=" * 80)
    print("RUNNING COMPREHENSIVE EVALUATION BENCHMARK")
    print("=" * 80)
    eval_result = evaluate_pipeline(engine, k=3)
    
    print("\nSUMMARY METRICS:")
    for metric, val in eval_result["summary"].items():
        print(f"  - {metric}: {val}")

    print("\nDETAILED PER-QUERY EVALUATION:")
    print(eval_result["details_df"].to_string(index=False))

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
