import streamlit as st
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUi:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            groq_model_options = self.config.get_groq_model_options()

            # LLM selection
            self.user_controls['llm_selection'] = st.selectbox(
                "Select LLM:",
                llm_options
            )
        
            if self.user_controls['llm_selection'] == 'Groq':
                # Model selection for Groq LLMs
                groq_model_options = self.config.get_groq_model_options()
                self.user_controls['groq_model_selection'] = st.selectbox(
                    "Select Model:",
                    groq_model_options
                )
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key:", type="password")
                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your Groq API Key to proceed.")
        

            self.user_controls['usecase_selection'] = st.selectbox(
                    "Select Use Case:",
                    usecase_options
            )
            return self.user_controls

