import os
import streamlit as st
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, user_controls):
        self.user_controls = user_controls

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls.get("GROQ_API_KEY")
            groq_model_name = self.user_controls.get("groq_model_selection")

            if not groq_api_key:
                st.error("Groq API Key is missing.")
                return None

            if not groq_model_name:
                st.error("Groq Model selection is missing.")
                return None

            llm = ChatGroq(
                model=groq_model_name,
                api_key=groq_api_key
            )
        except Exception as e:
            raise ValueError(f"Error Occurred with exception : {e} ")
        return llm