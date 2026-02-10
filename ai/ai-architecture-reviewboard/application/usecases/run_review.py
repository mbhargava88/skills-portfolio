from infrastructure.graph.state_graph import build_graph
from domain.entities import ReviewState

class RunReview:
    def __init__(self):
        self.graph = build_graph()

    def execute(self, problem: str) -> ReviewState:
        initial_state: ReviewState = {
            "problem": problem,
            "proposal": "",
            "critique": "",
            "score": 0,
            "iteration": 0,
            "final_architecture": None,
            "risk_register": None
        }
        
        # Stream the graph execution to see intermediate steps if needed
        # For now, just return the final state
        final_state = self.graph.invoke(initial_state)
        return final_state
