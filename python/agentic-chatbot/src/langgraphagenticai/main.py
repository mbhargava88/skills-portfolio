import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUi

def load_langgraph_agentic_ai_ui():
    """
    Loads & runs the LangGraph Agentic AI application with Streamlit UI.
    This function initializes the UI components, handles user interactions.
    """

    # Load UI
    ui_loader = LoadStreamlitUi()
    user_controls = ui_loader.load_streamlit_ui()

    if not user_controls:
        st.error("Failed to load user inputs from UI.")
    return 

    user_message = st.chat_input("Enter your message:")