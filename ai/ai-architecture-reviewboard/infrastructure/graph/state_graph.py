from langgraph.graph import StateGraph, END
from domain.entities import ReviewState
from application.agents.architect import ArchitectAgent
from application.agents.reviewer import ReviewerAgent

def build_graph():
    # Initialize agents
    architect = ArchitectAgent()
    reviewer = ReviewerAgent()

    # Define nodes
    workflow = StateGraph(ReviewState)
    
    workflow.add_node("architect", architect.propose_architecture)
    workflow.add_node("reviewer", reviewer.review_architecture)

    # Define edges
    workflow.set_entry_point("architect")
    
    workflow.add_edge("architect", "reviewer")
    
    def should_continue(state: ReviewState):
        if state["score"] >= 85 or state["iteration"] >= 3:
            return "finalize"
        return "refine"

    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "finalize": END,
            "refine": "architect"
        }
    )

    return workflow.compile()
