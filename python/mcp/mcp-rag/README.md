# RAG MCP Server (fastmcp + Groq + HuggingFace)

This project demonstrates a production-ready **Retrieval-Augmented Generation (RAG)** pipeline wrapped as an **MCP server**.

## Prerequisites
- A [Groq account](https://groq.com) with an active **API key**  
  (Export it as an environment variable, e.g., add `export GROQ_API_KEY=your_key_here` to your `~/.zshrc` or `~/.bashrc`)  
- Python 3.10 or later  
- Git  

## Features
- **Vector DB**: In-memory FAISS
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`
- **LLM**: Groq Gemma
- **MCP Tools**:
  - `add_details_to_vector_db`
  - `retrieve_from_vector_db`
  - `transform_with_groq_tool`

## Install
```bash
git clone <repo>
cd mcp-rag
python -m venv .venv
source .venv/bin/activate
pip install -e .
