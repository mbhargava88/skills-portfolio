import pytest
from unittest.mock import MagicMock
from src.application.recommendation_service import RecommendationService
from src.domain.entities import Product, Cart, Order, CartItem

@pytest.fixture
def mock_dependencies():
    product_repo = MagicMock()
    order_repo = MagicMock()
    vector_store = MagicMock()
    llm_service = MagicMock()
    
    return product_repo, order_repo, vector_store, llm_service

def test_recommendation_flow(mock_dependencies):
    product_repo, order_repo, vector_store, llm_service = mock_dependencies
    
    # Setup Data
    user_id = "UTest"
    cart = Cart(user_id=user_id)
    cart.items.append(CartItem(product_id="P_Cart"))
    
    # Mock Order History
    order_repo.get_orders_by_user.return_value = [
        Order(order_id="O1", user_id=user_id, product_ids=["P_Old"], timestamp="2024-01-01")
    ]
    
    # Mock Repo Returns
    product_repo.get_products_by_ids.side_effect = lambda ids: [
        Product(product_id=pid, name=f"Name_{pid}", category="Cat", description="Desc", price=10.0) 
        for pid in ids
    ]
    
    # Mock LLM
    llm_service.get_recommendations.return_value = "I recommend Product X because..."
    
    service = RecommendationService(product_repo, order_repo, vector_store, llm_service)
    
    # Act
    result = service.get_recommendations_for_user(user_id, cart)
    
    # Assert
    assert result == "I recommend Product X because..."
    
    # Verify Interactions
    order_repo.get_orders_by_user.assert_called_with(user_id)
    assert llm_service.get_recommendations.call_count == 1
