# RAG MCP Server (fastmcp + Groq + HuggingFace)

This project implements a **production-ready Retrieval-Augmented Generation (RAG) pipeline** packaged as an **MCP server**. It allows clients like Claude Desktop or Gemini Code Assistant to perform **semantic search and AI-powered transformations** on custom knowledge data.  

The server supports the following workflow:  
1. **Ingest knowledge**: Add text or documents to an in-memory FAISS vector database using **HuggingFace embeddings**.  
2. **Semantic retrieval**: Query the vector database to retrieve the most relevant information for a given prompt.  
3. **LLM transformation**: Transform the retrieved knowledge into natural language responses using **Groq LLM** (Gemma models).  

This setup enables a **modular RAG system** that can be easily integrated with MCP clients, allowing you to build **agentic AI workflows** that combine knowledge storage, retrieval, and LLM-based reasoning in one pipeline.


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


## Usage

Before using, make sure you have:
- A [Groq](https://groq.com/) account and a valid **GROQ_API_KEY** (export it in your shell, e.g. `export GROQ_API_KEY=your_key_here`).
- Your MCP client (e.g., Claude Desktop or Gemini Code Assistant) configured with this MCP server.

### Step-by-step Workflow Example (RAG Flow)

1. **Add details to the Vector DB**
   ```json
   {
     "tool": "add_details_to_vector_db",
     "params": {
       "text": "The Eiffel Tower is located in Paris and is 330 meters tall."
     }
   }

2. **Retrieve from the Vector DB**
{
  "tool": "retrieve_from_vector_db",
  "params": {
    "query": "Where is the Eiffel Tower located?"
  }
}

3. **Transform with Groq Tool**
{
  "tool": "transform_with_groq_tool",
  "params": {
    "prompt": "Summarize what we know about the Eiffel Tower."
  }
}


