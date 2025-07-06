from src.Agent.Graph.base_graph import BaseGraph
from langgraph.graph import StateGraph , END , START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from src.Agent.LLM.factory_providers import LLMFactory
from src.Agent.Nodes.assistant_node import AssistantNode
from src.Agent.Nodes.human_tool_review_node import HumanToolReviewNode
from src.Agent.Graph.Enumerations.nodes_name_enums import NodeName
from src.MCP import mcp_config
from src.Agent.LLM.LLMBuilder.llm_builder import LLMBuilder
from src.Agent.State.crm_state import AgentState

class CRMGraph(BaseGraph):
    
    def __init__(self):
        super().__init__()
        self.llm_builder = LLMBuilder(llm_name=self.settings.GENERATION_BACKEND , mcp_config=mcp_config)
        llm_with_tools , tools = self.llm_builder.build_llm()
        self.llm_with_tools = llm_with_tools
        self.tools = tools
        self.nodes = {NodeName.ASSISTANT_NODE.value : AssistantNode(llm=self.llm_with_tools) ,
                      NodeName.HUMAN_TOOL_REVIEW_NODE.value : HumanToolReviewNode() ,
                      NodeName.TOOLS.value : ToolNode(tools=self.tools)}
        

    def build_graph(self) -> StateGraph:
        graph = StateGraph(state_schema=AgentState)

        # Add nodes
        for node_name, node_instance in self.nodes.items():
            graph.add_node(node_name, node_instance)

        graph.add_edge(START, NodeName.ASSISTANT_NODE.value)
        graph.add_conditional_edges(NodeName.ASSISTANT_NODE.value, 
                                    self._assistant_router, 
                                    [NodeName.TOOLS.value, NodeName.HUMAN_TOOL_REVIEW_NODE.value, END])
        graph.add_edge(NodeName.TOOLS.value, NodeName.ASSISTANT_NODE.value)

        return graph.compile(checkpointer=MemorySaver())

    def get_graph(self) -> StateGraph:
        """Get the compiled graph"""
        if self.graph is None:
            self.graph = self.build_graph()
        return self.graph
    

    def _assistant_router(self,state: AgentState) -> str:
        last_message = state.messages[-1]
        if not last_message.tool_calls:
            return END
        else:
            if not state.yolo_mode:
                if any(tool_call["name"] in state.protected_tools for tool_call in last_message.tool_calls):
                    return NodeName.HUMAN_TOOL_REVIEW_NODE.value
            return NodeName.TOOLS.value

