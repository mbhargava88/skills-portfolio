import os
from typing import List
from groq import Groq
from src.domain.interfaces import LLMService
from src.domain.entities import Product

class GroqClient(LLMService):
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            # For local testing without key, we might want to handle this gracefully or raise error
            # But for production code, we expect the key.
            # We'll allow empty key and fail on call if not set, or relying on mock for tests.
            pass
        
        self.client = Groq(api_key=api_key) if api_key else None

    def get_recommendations(self, user_history: List[Product], current_cart: List[Product]) -> str:
        if not self.client:
            return "Error: Groq API Key not found."

        history_str = "\n".join([f"- {p.name} ({p.category})" for p in user_history])
        cart_str = "\n".join([f"- {p.name} ({p.category})" for p in current_cart])
        
        prompt = f"""
        You are an expert product recommender system.
        
        User Purchase History:
        {history_str}
        
        Current Shopping Cart:
        {cart_str}
        
        Based on the above, suggest 5 relevant products to recommend next.
        Explain WHY you selected each one briefly.
        Focus on complementary items or upgrades.
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI shopping assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant", # Using a supported Groq model
        )

        return chat_completion.choices[0].message.content
