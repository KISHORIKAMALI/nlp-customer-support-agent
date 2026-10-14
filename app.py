"""
Streamlit Web Application: LLM-Based Customer Support Chatbot
Features:
- Dual Modes: Normal Mode (Clean Customer View) vs Debug/Demo Mode (Transparent Agentic Trace)
- Fast-select buttons for all 6 Mandatory Demo Questions
- Live Inspection of:
  * Intent Detection & Confidence
  * Planning Agent sub-goals
  * Multi-source Hybrid Retrieval (Vector + BM25)
  * Semantic Re-ranking scores
  * Evidence Snippets & Grounding
  * Tool / API execution trace
  * Evidence Verification (Sufficiency & Contradiction Checking)
  * Response Latency
- Comprehensive Live Evaluation Dashboard with real metrics
"""

import streamlit as st
import time
import json
import pandas as pd
import sys
import os

# Ensure src & knowledge_base are on path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from knowledge_base.documents import DOCUMENTS
from src.document_processor import process_all_documents
from src.retrieval import HybridRetrievalPipeline
from src.agent_engine import SupportAgentEngine
from src.evaluation import evaluate_pipeline, EVALUATION_TEST_SUITE

# Page Configuration
st.set_page_config(
    page_title="AI Customer Support Agent | RAG + Agentic AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid #3B82F6;
        margin-bottom: 10px;
    }
    .badge-intent {
        background-color: #DBEAFE;
        color: #1D4ED8;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-verification {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-tool {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stChatMessage {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Cache initialization of pipeline
@st.cache_resource(show_spinner="Initializing SentenceTransformers, FAISS Index, and BM25 Corpus...")
def load_agent_engine():
    chunks = process_all_documents(DOCUMENTS)
    retrieval_pipeline = HybridRetrievalPipeline(model_name="all-MiniLM-L6-v2")
    retrieval_pipeline.initialize(chunks)
    engine = SupportAgentEngine(retrieval_pipeline)
    return engine, chunks

engine, chunks = load_agent_engine()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your AI Customer Support Assistant. How can I help you today with your orders, returns, warranty, or product queries?",
            "debug_info": None
        }
    ]

# Sidebar Controls
st.sidebar.title("⚙️ Agent Settings")
app_mode = st.sidebar.radio("Display Mode:", ["Normal User View", "Debug / Demo Agentic Trace"], index=1)

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Mandatory Demo Queries")
demo_queries = [
    "Can I return a damaged laptop?",
    "My order is ORD1001. Where is it?",
    "My order has not arrived. Can I cancel it and get a refund?",
    "Why was my refund rejected?",
    "I want to speak to a human.",
    "How long will the refund take?"
]

selected_demo = None
for dq in demo_queries:
    if st.sidebar.button(dq, key=f"btn_{dq}", use_container_width=True):
        selected_demo = dq

st.sidebar.markdown("---")
st.sidebar.subheader("📊 System Stats")
st.sidebar.info(
    f"• **Knowledge Docs:** {len(DOCUMENTS)}\n"
    f"• **Indexed Chunks:** {len(chunks)}\n"
    f"• **Dense Embeddings:** `all-MiniLM-L6-v2` (384-d)\n"
    f"• **Vector DB:** FAISS (Inner Product)\n"
    f"• **Lexical Index:** BM25Okapi\n"
    f"• **Multi-Agent:** Planner + Tools + Verifier"
)

# Header
st.markdown('<div class="main-header">🤖 Agentic Customer Support Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Transformers, Hybrid RAG (FAISS + BM25), Semantic Re-ranking, and Multi-Agent Reasoning</div>', unsafe_allow_html=True)

# Main layout tabs
tab_chat, tab_evaluation, tab_kb = st.tabs(["💬 Customer Chat", "📈 Evaluation Metrics", "📚 Knowledge Base & Mock Data"])

with tab_chat:
    # Display conversation messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # If Debug Mode is on and debug_info exists
            if app_mode == "Debug / Demo Agentic Trace" and msg.get("debug_info"):
                debug = msg["debug_info"]
                with st.expander("🔍 Agentic Execution Trace & RAG Telemetry", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"**Intent:** <span class='badge-intent'>{debug.get('intent')}</span>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**Confidence:** `{debug.get('confidence')}`")
                    with col3:
                        st.markdown(f"**Verification:** <span class='badge-verification'>{debug.get('verification', {}).get('status', 'PASSED')}</span>", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"**Response Latency:** `{debug.get('latency_seconds', 0.0)}s`")

                    st.markdown("#### 1. 📋 Planning Agent Sub-Goals")
                    for step in debug.get("plan", []):
                        st.markdown(f"- {step}")

                    if debug.get("rewritten_query") and debug.get("rewritten_query") != debug.get("user_query"):
                        st.markdown("#### 🔄 Contextual Query Rewriting")
                        st.info(f"**Rewritten Context Query:** `{debug.get('rewritten_query')}`")

                    st.markdown("#### 2. 🔍 Multi-Source Hybrid Retrieval & Re-ranking")
                    sources = debug.get("retrieval_sources", [])
                    st.write(f"**Retrieval Methods Activated:** {', '.join(set(sources)) if sources else 'None (Direct tool resolution)'}")

                    top_docs = debug.get("top_documents", [])
                    if top_docs:
                        doc_df = pd.DataFrame([
                            {
                                "Document Title": d["title"],
                                "Category": d["category"],
                                "Re-rank Score": d["score"],
                                "Source File": d["source"],
                                "Excerpt": d["snippet"]
                            }
                            for d in top_docs
                        ])
                        st.dataframe(doc_df, use_container_width=True)

                    st.markdown("#### 3. 🛠️ Dynamic Tools / APIs Invoked")
                    tools_used = debug.get("tools_called", {})
                    if tools_used:
                        for t_name, t_val in tools_used.items():
                            st.markdown(f"<span class='badge-tool'>Tool: {t_name}</span>", unsafe_allow_html=True)
                            st.json(t_val)
                    else:
                        st.write("No external tool required (satisfied by policy knowledge base).")

                    st.markdown("#### 4. 🛡️ Verification & Consistency Check")
                    st.json(debug.get("verification", {}))

    # User Query Input
    user_input = st.chat_input("Ask a question about your order, returns, warranty, or policies...")
    
    # Check if demo button was clicked
    query_to_run = selected_demo or user_input

    if query_to_run:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": query_to_run})
        with st.chat_message("user"):
            st.markdown(query_to_run)

        # Build context history for agent
        history_context = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
        ]

        with st.spinner("Agent planning, retrieving and verifying..."):
            result = engine.process_query(query_to_run, conversation_history=history_context)

        # Assistant response
        with st.chat_message("assistant"):
            st.markdown(result["final_response"])

            if app_mode == "Debug / Demo Agentic Trace":
                with st.expander("🔍 Agentic Execution Trace & RAG Telemetry", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"**Intent:** <span class='badge-intent'>{result.get('intent')}</span>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**Confidence:** `{result.get('confidence')}`")
                    with col3:
                        st.markdown(f"**Verification:** <span class='badge-verification'>{result.get('verification', {}).get('status', 'PASSED')}</span>", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"**Response Latency:** `{result.get('latency_seconds', 0.0)}s`")

                    st.markdown("#### 1. 📋 Planning Agent Sub-Goals")
                    for step in result.get("plan", []):
                        st.markdown(f"- {step}")

                    if result.get("rewritten_query") and result.get("rewritten_query") != result.get("user_query"):
                        st.markdown("#### 🔄 Contextual Query Rewriting")
                        st.info(f"**Rewritten Context Query:** `{result.get('rewritten_query')}`")

                    st.markdown("#### 2. 🔍 Multi-Source Hybrid Retrieval & Re-ranking")
                    top_docs = result.get("top_documents", [])
                    if top_docs:
                        doc_df = pd.DataFrame([
                            {
                                "Document Title": d["title"],
                                "Category": d["category"],
                                "Re-rank Score": d["score"],
                                "Source File": d["source"],
                                "Excerpt": d["snippet"]
                            }
                            for d in top_docs
                        ])
                        st.dataframe(doc_df, use_container_width=True)

                    st.markdown("#### 3. 🛠️ Dynamic Tools / APIs Invoked")
                    tools_used = result.get("tools_called", {})
                    if tools_used:
                        for t_name, t_val in tools_used.items():
                            st.markdown(f"<span class='badge-tool'>Tool: {t_name}</span>", unsafe_allow_html=True)
                            st.json(t_val)
                    else:
                        st.write("No external tool required.")

                    st.markdown("#### 4. 🛡️ Verification & Consistency Check")
                    st.json(result.get("verification", {}))

        # Save assistant message into state
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["final_response"],
            "debug_info": result
        })
        st.rerun()

with tab_evaluation:
    st.subheader("📊 End-to-End System Evaluation Benchmark")
    st.write("Evaluate Precision@K, Recall@K, MRR, Answer Relevance, Faithfulness/Groundedness, Task Completion, and Latency.")
    
    if st.button("🚀 Run Comprehensive Evaluation Benchmark", type="primary"):
        with st.spinner("Running live test suite across benchmark queries..."):
            eval_data = evaluate_pipeline(engine, k=3)
            
            st.success("Evaluation completed successfully on live data!")
            
            # Summary Metrics Row
            summary = eval_data["summary"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precision@3", f"{summary['Precision@3'] * 100:.1f}%")
            c2.metric("Recall@3", f"{summary['Recall@3'] * 100:.1f}%")
            c3.metric("MRR", f"{summary['MRR (Mean Reciprocal Rank)']:.3f}")
            c4.metric("Answer Relevance", f"{summary['Answer Relevance'] * 100:.1f}%")

            c5, c6, c7, c8 = st.columns(4)
            c5.metric("Faithfulness / Grounding", f"{summary['Faithfulness / Groundedness'] * 100:.1f}%")
            c6.metric("Task Completion Rate", f"{summary['Task Completion Rate'] * 100:.1f}%")
            c7.metric("Average Latency", f"{summary['Average Latency (seconds)']:.3f} s")
            c8.metric("Human Escalation Rate", f"{summary['Human Escalation Rate'] * 100:.1f}%")

            st.markdown("### 📋 Detailed Test Case Results")
            st.dataframe(eval_data["details_df"], use_container_width=True)

with tab_kb:
    st.subheader("📚 Knowledge Base Documents")
    for doc in DOCUMENTS:
        with st.expander(f"[{doc['category']}] {doc['title']}"):
            st.write(f"**Source:** `{doc['source']}`")
            st.write(doc["content"])

    st.markdown("---")
    st.subheader("📦 Mock CRM & Orders Database")
    from src.tools import ORDERS_DB, PRODUCTS_DB
    c_ord, c_prd = st.columns(2)
    with c_ord:
        st.write("**Orders Table (`ORDERS_DB`):**")
        st.json(ORDERS_DB)
    with c_prd:
        st.write("**Products Table (`PRODUCTS_DB`):**")
        st.json(PRODUCTS_DB)
