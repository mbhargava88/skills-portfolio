import streamlit as st
import sys
import os
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from infrastructure.graph.state_graph import build_graph

def main():
    st.set_page_config(page_title="AI Architecture Review Board", layout="wide")
    
    st.title("🏛️ AI Architecture Review Board")
    st.markdown("Simulating a design review between a **Principal Architect** and a **Chief Reviewer**.")

    # Load environment variables
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY environment variable not found. Please set it in your environment or .env file.")
        return

    # Input section
    problem = st.text_area("Problem Statement", height=100, placeholder="e.g. Design a scalable real-time chat application similar to WhatsApp.")
    
    start_btn = st.button("Start Review Session", type="primary")

    if start_btn and problem:
        st.divider()
        st.subheader("Discussion Log")
        
        graph = build_graph()
        
        initial_state = {
            "problem": problem,
            "proposal": "",
            "critique": "",
            "score": 0,
            "iteration": 0,
            "final_architecture": None,
            "risk_register": None
        }

        # Container to hold the conversation
        chat_container = st.container()

        with st.status("Review in progress...", expanded=True) as status:
            try:
                current_proposal = ""
                iteration_count = 0
                
                # Stream the graph execution
                for event in graph.stream(initial_state):
                    for node, state in event.items():
                        if node == "architect":
                            iteration_count = state.get("iteration", 0)
                            current_proposal = state.get("proposal", "")
                            
                            with chat_container:
                                with st.chat_message("user", avatar="🏗️"):
                                    st.write(f"**Principal Architect (Iteration {iteration_count})**")
                                    st.markdown(current_proposal)
                                    status.update(label=f"Architect proposed design (Iteration {iteration_count})")
                                    time.sleep(2)  # Pause for readability
                        
                        elif node == "reviewer":
                            critique = state.get("critique", "")
                            score = state.get("score", 0)
                            
                            with chat_container:
                                with st.chat_message("assistant", avatar="🧐"):
                                    st.write(f"**Chief Reviewer (Score: {score}/100)**")
                                    if score >= 85:
                                        st.success(f"✅ Architecture Approved! Final Score: {score}")
                                    else:
                                        st.warning(f"⚠️ Revisions requested. Score: {score}")
                                        status.update(label=f"Reviewer provided critique (Score: {score})")
                                    time.sleep(2)  # Pause for readability

                status.update(label="Review Session Completed", state="complete")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
