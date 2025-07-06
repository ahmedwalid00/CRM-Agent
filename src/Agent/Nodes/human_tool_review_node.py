from src.Agent.Nodes.base_node import BaseNode
from src.Agent.State.crm_state import AgentState

from langchain_core.messages import AIMessage,ToolMessage
from langgraph.types import Command, interrupt

import json

class HumanToolReviewNode(BaseNode):
    
    async def execute(self, state: AgentState) :
        last_message = state.messages[-1]
        tool_call = last_message.tool_calls[-1]

        human_review: dict = interrupt({
            "message": "Your input is required for the following tool:",
            "tool_call": tool_call
        })

        review_action = human_review["action"]
        review_data = human_review.get("data")

        if review_action == "continue":
            return Command(goto="tools")
        
        # Change the tool call arguments created by our Agent
        elif review_action == "update":
            
            updated_message = AIMessage(
                content=last_message.content,
                tool_calls=[{
                    "id": tool_call["id"],
                    "name": tool_call["name"],
                    "args": json.loads(review_data)
                }],
                id=last_message.id
            )

            return Command(goto="tools", update={"messages": [updated_message]})
        
        # Send feedback to the Agent as a tool message (required after a tool call)
        elif review_action == "feedback":
            
            tool_message = ToolMessage(
                content=review_data,
                name=tool_call["name"],
                tool_call_id=tool_call["id"]
            )
            return Command(goto="assistant_node", update={"messages": [tool_message]})