from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Product, Order, Cart

class ProductRepository(ABC):
    @abstractmethod
    def get_product(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def search_products(self, query: str, limit: int = 5) -> List[Product]:
        pass
    
    @abstractmethod
    def get_products_by_ids(self, product_ids: List[str]) -> List[Product]:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def get_orders_by_user(self, user_id: str) -> List[Order]:
        pass

class VectorStore(ABC):
    @abstractmethod
    def search_similar_products(self, product_embedding: List[float], limit: int = 5) -> List[str]:
        # Returns list of product_ids
        pass

class LLMService(ABC):
    @abstractmethod
    def get_recommendations(self, user_history: List[Product], current_cart: List[Product]) -> str:
        pass
