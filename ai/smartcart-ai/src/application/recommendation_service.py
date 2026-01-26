from typing import List
from src.domain.entities import Product, User, Cart
from src.domain.interfaces import ProductRepository, OrderRepository, VectorStore, LLMService

class RecommendationService:
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        vector_store: VectorStore,
        llm_service: LLMService
    ):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.vector_store = vector_store
        self.llm_service = llm_service

    def get_recommendations_for_user(self, user_id: str, current_cart: Cart) -> str:
        # 1. Get User History
        orders = self.order_repo.get_orders_by_user(user_id)
        purchased_product_ids = []
        for order in orders:
            purchased_product_ids.extend(order.product_ids)
        
        # Get unique recent purchases (last 5)
        recent_product_ids = list(set(purchased_product_ids))[-5:]
        user_history = self.product_repo.get_products_by_ids(recent_product_ids)

        # 2. Get Cart Items
        cart_product_ids = [item.product_id for item in current_cart.items]
        current_cart_products = self.product_repo.get_products_by_ids(cart_product_ids)

        # 3. (Optional) Vector Search for similar candidates
        # For this prototype we will skip the actual embedding generation here 
        # and rely on the LLM to pick from global knowledge or context we provide.
        # In a real app, we would:
        # embedding = create_embedding(user_history)
        # candidates = vector_store.search(embedding)
        # filtered_candidates = product_repo.get(candidates)
        
        # 4. LLM Reasoning
        recommendation_text = self.llm_service.get_recommendations(
            user_history=user_history,
            current_cart=current_cart_products
        )
        
        return recommendation_text
