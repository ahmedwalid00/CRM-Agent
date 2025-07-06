from pydantic import BaseModel
from typing import Annotated , List 
from langgraph.graph.message import add_messages, BaseMessage

class  AgentState(BaseModel):
    """The state of the agent.
    
    Attributes:
        messages: The list of messages in the conversation.
        yolo_mode: Whether to skip human review of protected tool calls.
    """
    messages: Annotated[List[BaseMessage], add_messages] = []
    protected_tools: List[str] = ["create_campaign", "send_campaign_email"]
    yolo_mode: bool = False