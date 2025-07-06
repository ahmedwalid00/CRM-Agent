from abc import ABC , abstractmethod
from src.Agent.State.crm_state import AgentState
from typing import List , Dict , Any
from src.Agent.LLM.base_factory_provider import BaseLLMFactory

class BaseNode(ABC):
    """Base class for all CRM nodes"""
    
    @abstractmethod
    async def execute(self, state: AgentState) :
        """Execute the node logic"""
        pass
    
    def __call__(self, state: AgentState) :
        """Make the node callable"""
        return self.execute(state)