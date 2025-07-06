from src.Agent.LLM.factory_providers import LLMFactory
from src.Agent.LLM.LLMBuilder.base_llm_builder import BaseLLMBuilder


class LLMBuilder(BaseLLMBuilder):
    
    def __init__(self , llm_name : str , mcp_config = None):
        super().__init__()
        self.llm_name = llm_name
        self.mcp_config = mcp_config if mcp_config else None

    def build_llm(self):
        llm_factory = LLMFactory()
        llm_provider = llm_factory.create_llm_provider(llm_name=self.llm_name)
        if self.mcp_config :
            print("Creating LLM With MCP Tools")
            _ = llm_provider.initialize_llm_mcptools(mcp_config=self.mcp_config)
            llm_with_tools = llm_provider.llm_with_tools
            tools = llm_provider.tools

            return llm_with_tools , tools
        
        _ = llm_provider.initialize_llm()
        print("Creating LLm")
        llm = llm_provider.llm
        return llm

