import pandas as pd
from typing import List, Dict
from src.domain.entities import Product, Order

class CSVLoader:
    def __init__(self, products_path: str, orders_path: str):
        self.products_path = products_path
        self.orders_path = orders_path
        self.products_df = None
        self.orders_df = None

    def load_data(self):
        self.products_df = pd.read_csv(self.products_path)
        self.orders_df = pd.read_csv(self.orders_path)

    def get_products(self) -> List[Product]:
        if self.products_df is None:
            self.load_data()
        
        products = []
        for _, row in self.products_df.iterrows():
            products.append(Product(
                product_id=str(row['product_id']),
                name=row['name'],
                category=row['category'],
                description=row['description'],
                price=float(row['price'])
            ))
        return products

    def get_orders(self) -> List[Order]:
        if self.orders_df is None:
            self.load_data()
        
        orders = []
        # Group by order_id to aggregate products
        grouped = self.orders_df.groupby('order_id')
        for order_id, group in grouped:
            orders.append(Order(
                order_id=str(order_id),
                user_id=str(group.iloc[0]['user_id']),
                product_ids=group['product_id'].astype(str).tolist(),
                timestamp=pd.to_datetime(group.iloc[0]['timestamp'])
            ))
        return orders
