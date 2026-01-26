import pandas as pd
from src.infrastructure.db.csv_loader import CSVLoader
import os

def test_csv_loader(tmp_path):
    # Create temp CSVs
    p_file = tmp_path / "products.csv"
    p_file.write_text("product_id,name,category,description,price\nP1,TestProd,Cat,Desc,100.0")
    
    o_file = tmp_path / "orders.csv"
    o_file.write_text("order_id,user_id,product_id,timestamp\nO1,U1,P1,2024-01-01")
    
    loader = CSVLoader(str(p_file), str(o_file))
    
    products = loader.get_products()
    orders = loader.get_orders()
    
    assert len(products) == 1
    assert products[0].name == "TestProd"
    assert products[0].price == 100.0
    
    assert len(orders) == 1
    assert orders[0].user_id == "U1"
    assert orders[0].product_ids == ["P1"]
