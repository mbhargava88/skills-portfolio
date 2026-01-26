from src.domain.entities import Cart, CartItem

def test_cart_total_items():
    cart = Cart(user_id="U1")
    cart.items.append(CartItem(product_id="P1", quantity=2))
    cart.items.append(CartItem(product_id="P2", quantity=1))
    
    assert cart.total_items == 3

def test_cart_initialization():
    cart = Cart(user_id="U2")
    assert cart.user_id == "U2"
    assert len(cart.items) == 0
