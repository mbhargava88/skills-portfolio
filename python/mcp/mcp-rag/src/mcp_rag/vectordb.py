import faiss
import numpy as np

class VectorDB:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.text_store = []

    def add(self, text, embedding):
        self.index.add(np.array([embedding]).astype("float32"))
        self.text_store.append(text)

    def search(self, query_embedding, top_k=3):
        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"), top_k
        )
        return [self.text_store[i] for i in I[0] if i < len(self.text_store)]
