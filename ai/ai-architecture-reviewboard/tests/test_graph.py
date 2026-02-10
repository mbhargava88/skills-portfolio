import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domain.entities import ReviewState
from application.agents.architect import ArchitectAgent
from application.agents.reviewer import ReviewerAgent
from infrastructure.graph.state_graph import build_graph

class TestReviewBoard(unittest.TestCase):

    @patch('application.agents.architect.GroqClient')
    @patch('application.agents.reviewer.GroqClient')
    def test_graph_execution(self, mock_reviewer_client, mock_architect_client):
        # Mock Architect LLM response
        mock_arch_llm = MagicMock()
        mock_arch_llm.invoke.return_value.content = "Proposed Architecture"
        mock_architect_client.return_value.get_llm.return_value = mock_arch_llm

        # Mock Reviewer LLM response (first iteration low score, second high score)
        mock_rev_llm = MagicMock()
        
        resp1 = MagicMock()
        resp1.content = "Critique 1\nSCORE: 50"
        
        resp2 = MagicMock()
        resp2.content = "Critique 2\nSCORE: 90"
        
        # Side effect: first call returns low score, second call returns high score (finalize)
        mock_rev_llm.side_effect = [resp1, resp2]
        mock_rev_llm.invoke.side_effect = [resp1, resp2]
        mock_reviewer_client.return_value.get_llm.return_value = mock_rev_llm

        # Build graph
        graph = build_graph()
        
        # Run graph
        initial_state = {
            "problem": "Test Problem",
            "iteration": 0,
            "score": 0,
            "proposal": "",
            "critique": ""
        }
        
        final_state = graph.invoke(initial_state)
        
        # Verify
        self.assertGreaterEqual(final_state["score"], 85)
        self.assertGreater(final_state["iteration"], 0)
        print(f"Final Score: {final_state['score']}")
        print(f"Iterations: {final_state['iteration']}")

if __name__ == '__main__':
    unittest.main()
