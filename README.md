# Knowledge Base Q&A Bot

A RAG pipeline that answers questions grounded in Markdown documents.

## Architecture
docs/ → indexer.py → .kb/index.json → retriever.py → qa.py → Answer + Citation

## Stack
- Retrieval: BM25 with stop-word filtering, stemming, and synonym expansion
- LLM: OpenAI GPT-4o-mini
- Language: Python 3.10+

## Setup
pip install -r requirements.txt
python indexer.py
python qa.py

## What I learned
- BM25 fails on synonyms ("money back" ≠ "refund") → solved with query expansion
- RAG quality depends on retrieval, not just the LLM
- Prompt engineering matters even when retrieval is correct
- Next: Vector Search with OpenAI Embeddings + FAISS

## Roadmap
- [x] Markdown indexer
- [x] BM25 retrieval with stop-words, stemming, synonym expansion  
- [x] OpenAI GPT grounded QA with citation
- [ ] Vector Search with OpenAI Embeddings
- [ ] FAISS vector store
- [ ] FastAPI endpoint
- [ ] Hybrid Search (BM25 + Vector)