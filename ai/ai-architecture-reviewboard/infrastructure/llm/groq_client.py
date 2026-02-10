import os
from langchain_groq import ChatGroq

class GroqClient:
    def __init__(self, temperature: float = 0.6, model: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model,
            groq_api_key=api_key
        )

    def get_llm(self):
        return self.llm
