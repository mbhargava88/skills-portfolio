from abc import ABC, abstractmethod
from typing import Any, Dict

class AgentPort(ABC):
    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
