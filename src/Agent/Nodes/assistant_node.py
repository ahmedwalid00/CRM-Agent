from src.Agent.Nodes.base_node import BaseNode
from src.Agent.LLM.LLMProviders.base_provider import BaseProvider
from src.Agent.State.crm_state import AgentState
from src.Agent.Prompts.agent_prompts import agent_system_prompt

from langchain_core.messages import SystemMessage


class AssistantNode(BaseNode):
    
    def __init__(self , llm : BaseProvider):
        self._llm = llm
    

    async def execute(self, state: AgentState) :
        response = self._llm.invoke(
            [SystemMessage(content=agent_system_prompt)] +
            state.messages
            )
        state.messages = state.messages + [response]
        return state
    


