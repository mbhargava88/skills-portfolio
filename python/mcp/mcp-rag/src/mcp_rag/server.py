from dotenv import load_dotenv
load_dotenv()

from fastmcp import FastMCP
from .vectordb import VectorDB
from .embeddings import embed_text
from .groq_client import transform_with_groq
from dataclasses import dataclass

@dataclass
class AddDetailsResponse:
    status: str
    saved_text: str

mcp = FastMCP("RAG-MCP-Server")
db = VectorDB()

@mcp.tool()
def add_details_to_vectordb(text:str) -> AddDetailsResponse:
    """embed text and add to vector database.   

    Args:
        text (str): The text to be embedded and add to the vector database.
    """
    embedding = embed_text(text)
    db.add(text, embedding)
    return AddDetailsResponse(status="ok", saved_text=text)

@mcp.tool()
def retrieve_from_vector_db(query: str, top_k: int = 3):
    """Retrieve semantically similar texts from vector DB."""
    query_embedding = embed_text(query)
    results = db.search(query_embedding, top_k)
    return {"matches": results}

@mcp.tool()
def transform_with_groq_tool(query: str):
    """Retrieve from DB and transform using Groq LLM."""
    query_embedding = embed_text(query)
    results = db.search(query_embedding, 3)
    context = "\n".join(results)
    prompt = f"Use the following context to answer:\n{context}\n\nQuery: {query}"
    return transform_with_groq(prompt)

def main():
    mcp.run()

if __name__ == "__main__":
    main()

