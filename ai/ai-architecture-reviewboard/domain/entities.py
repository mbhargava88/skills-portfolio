from typing import TypedDict, Optional, List, Dict, Any

class ReviewState(TypedDict):
    problem: str
    proposal: str
    critique: str
    score: int
    iteration: int
    final_architecture: Optional[str]
    risk_register: Optional[List[str]]
