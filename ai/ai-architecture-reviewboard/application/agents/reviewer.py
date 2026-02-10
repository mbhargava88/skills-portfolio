from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from domain.entities import ReviewState
from infrastructure.llm.groq_client import GroqClient
import json
import re

class ReviewerAgent:
    def __init__(self):
        self.llm = GroqClient(temperature=0.2).get_llm()

    def review_architecture(self, state: ReviewState) -> ReviewState:
        proposal = state["proposal"]
        
        prompt = ChatPromptTemplate.from_template(
            """You are a Chief Architecture Reviewer.
            Review the following architecture critically:
            
            {proposal}
            
            Evaluate on:
            1. Scalability
            2. Resilience
            3. Security
            4. Cost efficiency
            5. Observability
            6. Maintainability
            
            Provide:
            - Top risks
            - Missing components
            - Concrete improvement suggestions
            - Readiness score (0-100)
            
            IMPORTANT: At the very end of your response, output the score strictly in this format:
            SCORE: <integer>
            """
        )
        
        chain = prompt | self.llm
        response = chain.invoke({"proposal": proposal})
        content = response.content
        
        # Extract score
        score_match = re.search(r"SCORE:\s*(\d+)", content)
        score = int(score_match.group(1)) if score_match else 0
        
        state["critique"] = content
        state["score"] = score
        return state
