crm_agent/
├── nodes/
│   ├── __init__.py
│   ├── base_node.py
│   ├── customer_service_node.py
│   ├── lead_qualification_node.py
│   ├── data_retrieval_node.py
│   └── escalation_node.py
├── graphs/
│   ├── __init__.py
│   ├── base_graph.py
│   └── crm_workflow_graph.py
├── states/
│   ├── __init__.py
│   └── crm_state.py
├── tools/
│   ├── __init__.py
│   └── mcp_tools.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── main.py

# Example implementation files:

## 1. states/crm_state.py
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from langgraph.graph import MessagesState

class CRMState(MessagesState):
    """Extended state for CRM operations"""
    customer_id: Optional[str] = None
    lead_score: Optional[float] = None
    interaction_type: Optional[str] = None
    escalation_required: bool = False
    context: Dict[str, Any] = {}
    next_action: Optional[str] = None

## 2. nodes/base_node.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from ..states.crm_state import CRMState

class BaseNode(ABC):
    """Base class for all CRM nodes"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, state: CRMState) -> Dict[str, Any]:
        """Execute the node logic"""
        pass
    
    def __call__(self, state: CRMState) -> Dict[str, Any]:
        """Make the node callable"""
        return self.execute(state)

## 3. nodes/customer_service_node.py
from typing import Dict, Any
from .base_node import BaseNode
from ..states.crm_state import CRMState
from ..tools.mcp_tools import MCPTools

class CustomerServiceNode(BaseNode):
    """Node for handling customer service interactions"""
    
    def __init__(self):
        super().__init__("customer_service")
        self.mcp_tools = MCPTools()
    
    async def execute(self, state: CRMState) -> Dict[str, Any]:
        """Handle customer service logic"""
        try:
            # Get customer data
            customer_data = await self.mcp_tools.get_customer_data(state.customer_id)
            
            # Analyze the customer's message
            last_message = state.messages[-1] if state.messages else None
            
            # Determine if escalation is needed
            escalation_needed = self._needs_escalation(last_message, customer_data)
            
            # Generate response
            response = await self._generate_response(last_message, customer_data)
            
            return {
                "messages": [response],
                "escalation_required": escalation_needed,
                "context": {
                    "customer_data": customer_data,
                    "service_type": "customer_support"
                }
            }
            
        except Exception as e:
            return {
                "messages": [f"Error in customer service: {str(e)}"],
                "escalation_required": True
            }
    
    def _needs_escalation(self, message: Any, customer_data: Dict) -> bool:
        """Determine if escalation is needed"""
        # Implementation logic here
        return False
    
    async def _generate_response(self, message: Any, customer_data: Dict) -> str:
        """Generate appropriate response"""
        # Implementation logic here
        return "Thank you for contacting us. How can I help you today?"

## 4. nodes/lead_qualification_node.py
from typing import Dict, Any
from .base_node import BaseNode
from ..states.crm_state import CRMState
from ..tools.mcp_tools import MCPTools

class LeadQualificationNode(BaseNode):
    """Node for qualifying leads"""
    
    def __init__(self):
        super().__init__("lead_qualification")
        self.mcp_tools = MCPTools()
    
    async def execute(self, state: CRMState) -> Dict[str, Any]:
        """Qualify leads based on interaction"""
        try:
            # Extract lead information
            lead_info = await self._extract_lead_info(state.messages)
            
            # Calculate lead score
            lead_score = self._calculate_lead_score(lead_info)
            
            # Determine next action
            next_action = self._determine_next_action(lead_score)
            
            return {
                "lead_score": lead_score,
                "next_action": next_action,
                "context": {
                    "lead_info": lead_info,
                    "qualification_complete": True
                }
            }
            
        except Exception as e:
            return {
                "messages": [f"Error in lead qualification: {str(e)}"],
                "escalation_required": True
            }
    
    async def _extract_lead_info(self, messages: List) -> Dict:
        """Extract relevant lead information from messages"""
        # Implementation logic here
        return {}
    
    def _calculate_lead_score(self, lead_info: Dict) -> float:
        """Calculate lead score based on various factors"""
        # Implementation logic here
        return 0.5
    
    def _determine_next_action(self, lead_score: float) -> str:
        """Determine next action based on lead score"""
        if lead_score >= 0.7:
            return "schedule_demo"
        elif lead_score >= 0.4:
            return "nurture_lead"
        else:
            return "collect_more_info"

## 5. graphs/base_graph.py
from abc import ABC, abstractmethod
from langgraph.graph import Graph
from ..states.crm_state import CRMState

class BaseGraph(ABC):
    """Base class for all CRM graphs"""
    
    def __init__(self):
        self.graph: Graph = None
    
    @abstractmethod
    def build_graph(self) -> Graph:
        """Build the graph structure"""
        pass
    
    def get_graph(self) -> Graph:
        """Get the compiled graph"""
        if self.graph is None:
            self.graph = self.build_graph()
        return self.graph

## 6. graphs/crm_workflow_graph.py
from langgraph.graph import Graph, START, END
from .base_graph import BaseGraph
from ..nodes.customer_service_node import CustomerServiceNode
from ..nodes.lead_qualification_node import LeadQualificationNode
from ..nodes.data_retrieval_node import DataRetrievalNode
from ..nodes.escalation_node import EscalationNode
from ..states.crm_state import CRMState

class CRMWorkflowGraph(BaseGraph):
    """Main CRM workflow graph"""
    
    def __init__(self):
        super().__init__()
        self.nodes = {
            "customer_service": CustomerServiceNode(),
            "lead_qualification": LeadQualificationNode(),
            "data_retrieval": DataRetrievalNode(),
            "escalation": EscalationNode()
        }
    
    def build_graph(self) -> Graph:
        """Build the CRM workflow graph"""
        graph = Graph()
        
        # Add nodes
        for node_name, node_instance in self.nodes.items():
            graph.add_node(node_name, node_instance)
        
        # Add edges
        graph.add_edge(START, "data_retrieval")
        graph.add_conditional_edges(
            "data_retrieval",
            self._route_after_data_retrieval,
            {
                "customer_service": "customer_service",
                "lead_qualification": "lead_qualification",
                "escalation": "escalation"
            }
        )
        
        graph.add_conditional_edges(
            "customer_service",
            self._route_after_customer_service,
            {
                "escalation": "escalation",
                "end": END
            }
        )
        
        graph.add_conditional_edges(
            "lead_qualification",
            self._route_after_lead_qualification,
            {
                "customer_service": "customer_service",
                "end": END
            }
        )
        
        graph.add_edge("escalation", END)
        
        return graph.compile()
    
    def _route_after_data_retrieval(self, state: CRMState) -> str:
        """Route after data retrieval based on context"""
        interaction_type = state.interaction_type
        
        if interaction_type == "lead":
            return "lead_qualification"
        elif interaction_type == "support":
            return "customer_service"
        else:
            return "escalation"
    
    def _route_after_customer_service(self, state: CRMState) -> str:
        """Route after customer service"""
        if state.escalation_required:
            return "escalation"
        return "end"
    
    def _route_after_lead_qualification(self, state: CRMState) -> str:
        """Route after lead qualification"""
        next_action = state.next_action
        
        if next_action in ["schedule_demo", "complex_inquiry"]:
            return "customer_service"
        return "end"

## 7. main.py
import asyncio
from graphs.crm_workflow_graph import CRMWorkflowGraph
from states.crm_state import CRMState

class CRMAgent:
    """Main CRM Agent class"""
    
    def __init__(self):
        self.workflow_graph = CRMWorkflowGraph()
        self.graph = self.workflow_graph.get_graph()
    
    async def process_interaction(self, initial_state: CRMState) -> CRMState:
        """Process a customer interaction"""
        result = await self.graph.ainvoke(initial_state)
        return result
    
    async def stream_interaction(self, initial_state: CRMState):
        """Stream the interaction processing"""
        async for step in self.graph.astream(initial_state):
            yield step

# Usage example
async def main():
    agent = CRMAgent()
    
    # Example interaction
    initial_state = CRMState(
        messages=["Hello, I'm interested in your product"],
        customer_id="12345",
        interaction_type="lead"
    )
    
    result = await agent.process_interaction(initial_state)
    print(f"Final state: {result}")

if __name__ == "__main__":
    asyncio.run(main())