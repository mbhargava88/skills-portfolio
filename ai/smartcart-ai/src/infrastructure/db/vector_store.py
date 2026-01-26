import chromadb
from typing import List
from src.domain.interfaces import VectorStore

class ChromaVectorStore(VectorStore):
    def __init__(self, collection_name: str = "products"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_products(self, products: List[dict], embeddings: List[List[float]]):
        ids = [p['id'] for p in products]
        documents = [p['description'] for p in products]
        metadatas = [p['metadata'] for p in products]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def search_similar_products(self, product_embedding: List[float], limit: int = 5) -> List[str]:
        results = self.collection.query(
            query_embeddings=[product_embedding],
            n_results=limit
        )
        # Chroma returns lists of lists for queries
        if results['ids']:
            return results['ids'][0]
        return []
