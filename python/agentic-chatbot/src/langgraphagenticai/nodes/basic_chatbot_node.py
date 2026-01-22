
from langgraphagenticai.state.state import State

class BasicChatBotNode:
    """
    Basic chatbot login implementation.
    """
    def __init__(self, model,client, model_name):
        self.llm = model
        self.client = client
        self.model_name = model_name

    def process(self, state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": self.llm.invoke(state['messages'])}