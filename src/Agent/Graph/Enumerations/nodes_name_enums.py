from enum import Enum

class NodeName(Enum):
    ASSISTANT_NODE = "assistant_node"
    HUMAN_TOOL_REVIEW_NODE = "human_tool_review_node"
    TOOLS = "tools"