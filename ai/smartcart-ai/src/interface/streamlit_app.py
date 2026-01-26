import streamlit as st
import os
import pandas as pd
from typing import List

# Add project root to path if needed, though poetry run handles this usually
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.infrastructure.db.csv_loader import CSVLoader
from src.infrastructure.repositories.in_memory_repos import InMemoryProductRepository, InMemoryOrderRepository
from src.infrastructure.db.vector_store import ChromaVectorStore
from src.infrastructure.llm.groq_client import GroqClient
from src.application.recommendation_service import RecommendationService
from src.domain.entities import Cart, CartItem, Product

# Page Configuration
st.set_page_config(page_title="SmartCart AI", layout="wide")

# Session State Initialization
if "cart" not in st.session_state:
    # Dummy User ID for this session
    st.session_state.cart = Cart(user_id="U001") 

# Dependency Injection (Simple for Demo)
@st.cache_resource
def get_dependencies():
    # Load Data
    csv_loader = CSVLoader(
        products_path="data/products.csv",
        orders_path="data/orders.csv"
    )
    
    # Repos
    product_repo = InMemoryProductRepository(csv_loader)
    order_repo = InMemoryOrderRepository(csv_loader)
    
    # Vector DB (Init only)
    vector_store = ChromaVectorStore()
    
    return product_repo, order_repo, vector_store

product_repo, order_repo, vector_store = get_dependencies()

# --- SIDEBAR ---
with st.sidebar:
    st.title("SmartCart AI 🛒")
    st.write("LLM Powered Recommendations")
    
    api_key = st.text_input("Enter Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    
    st.divider()
    st.write(f"User: {st.session_state.cart.user_id}")
    st.write(f"Cart Items: {st.session_state.cart.total_items}")

# --- MAIN CONTENT ---
st.title("Product Catalog")

# 1. Product Listing
products = product_repo.search_products(query="") # Get all (limit logic inside repo specific to implementation)
# Actually the mock repo search returns matched items, let's just get all if query is empty
# Fixing the repo logic slightly or just iterate. 
# The repo search_products with empty string returns all in my impl? 
# "query.lower() in p.name.lower()" -> "" is in "anything" -> True. Yes.

cols = st.columns(3)
for idx, product in enumerate(products):
    with cols[idx % 3]:
        with st.container(border=True):
            st.subheader(product.name)
            st.write(f"**Category:** {product.category}")
            st.write(f"**Price:** ${product.price}")
            st.write(product.description)
            if st.button(f"Add to Cart", key=f"add_{product.product_id}"):
                st.session_state.cart.items.append(CartItem(product_id=product.product_id))
                st.toast(f"Added {product.name} to cart!")
                st.rerun()

st.divider()

# 2. Cart Section
st.header("Your Cart")
if not st.session_state.cart.items:
    st.info("Your cart is empty.")
else:
    cart_items_data = []
    for item in st.session_state.cart.items:
        p = product_repo.get_product(item.product_id)
        if p:
            cart_items_data.append({
                "Name": p.name,
                "Price": p.price,
                "Qty": item.quantity
            })
    st.table(pd.DataFrame(cart_items_data))

# 3. Recommendations
st.header("Recommended for You 🤖")

if st.button("Generate Recommendations"):
    if not api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
    else:
        with st.spinner("AI is thinking..."):
            llm_service = GroqClient(api_key=api_key)
            rec_service = RecommendationService(
                product_repo=product_repo,
                order_repo=order_repo,
                vector_store=vector_store,
                llm_service=llm_service
            )
            
            try:
                recommendations = rec_service.get_recommendations_for_user(
                    user_id=st.session_state.cart.user_id,
                    current_cart=st.session_state.cart
                )
                st.markdown(recommendations)
            except Exception as e:
                st.error(f"Error generating recommendations: {e}")

