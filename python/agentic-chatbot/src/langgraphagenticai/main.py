import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUi
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agentic_ai_ui():
    """
    Loads & runs the LangGraph Agentic AI application with Streamlit UI.
    This function initializes the UI components, handles user interactions.
    """

    ## Load UI
    ui_loader = LoadStreamlitUi()
    user_controls = ui_loader.load_streamlit_ui()

    if not user_controls:
        st.error("Failed to load user inputs from UI.")
        return 

    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            ## Configure the LLMs
            obj_llm_config=GroqLLM(user_controls=user_controls)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            ## Initialize and setup the graph based on use case
            usecase=user_controls.get("usecase_selection")

            if not usecase:
                st.error("Error: No usecase selected")

            ## Initialize graph builder
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed - {e}")
                return
        except Exception as e:
                st.error(f"Error: Graph set up failed - {e}")
                return     