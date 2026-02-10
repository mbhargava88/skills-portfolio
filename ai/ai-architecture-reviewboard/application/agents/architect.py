from langchain_core.prompts import ChatPromptTemplate
from domain.entities import ReviewState
from infrastructure.llm.groq_client import GroqClient

class ArchitectAgent:
    def __init__(self):
        self.llm = GroqClient(temperature=0.6).get_llm()

    def propose_architecture(self, state: ReviewState) -> ReviewState:
        problem = state["problem"]
        critique = state.get("critique", "")
        iteration = state.get("iteration", 0)

        pass  # Placeholder for prompt logic
        
        prompt = ChatPromptTemplate.from_template(
            """You are a Principal Software Architect.
            Design a production-grade system for the following problem:
            
            {problem}
            
            Previous Critique (if any):
            {critique}
            
            Constraints:
            - Cloud native
            - Secure by design
            - Cost efficient
            - Observable (metrics, logs, traces)
            
            Output:
            - Architecture overview
            - Component diagram (text)
            - Data flow
            - Technology choices
            - Key trade-offs
            """
        )
        
        chain = prompt | self.llm
        response = chain.invoke({"problem": problem, "critique": critique})
        
        state["proposal"] = response.content
        state["iteration"] = iteration + 1
        return state
