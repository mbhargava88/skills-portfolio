from typing import List, Optional
from src.domain.entities import Product, Order
from src.domain.interfaces import ProductRepository, OrderRepository
from src.infrastructure.db.csv_loader import CSVLoader

class InMemoryProductRepository(ProductRepository):
    def __init__(self, csv_loader: CSVLoader):
        self.csv_loader = csv_loader
        self._products = None

    def _ensure_loaded(self):
        if self._products is None:
            self._products = self.csv_loader.get_products()

    def get_product(self, product_id: str) -> Optional[Product]:
        self._ensure_loaded()
        for p in self._products:
            if p.product_id == product_id:
                return p
        return None

    def search_products(self, query: str, limit: int = 5) -> List[Product]:
        self._ensure_loaded()
        # Simple substring search for now
        results = [
            p for p in self._products 
            if query.lower() in p.name.lower() or query.lower() in p.description.lower()
        ]
        return results[:limit]
    
    def get_products_by_ids(self, product_ids: List[str]) -> List[Product]:
        self._ensure_loaded()
        return [p for p in self._products if p.product_id in product_ids]

class InMemoryOrderRepository(OrderRepository):
    def __init__(self, csv_loader: CSVLoader):
        self.csv_loader = csv_loader
        self._orders = None
    
    def _ensure_loaded(self):
        if self._orders is None:
            self._orders = self.csv_loader.get_orders()

    def get_orders_by_user(self, user_id: str) -> List[Order]:
        self._ensure_loaded()
        return [o for o in self._orders if o.user_id == user_id]
