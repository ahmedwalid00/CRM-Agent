from src.Agent.LLM.LLMProviders.base_provider import BaseProvider
from langchain_openai import ChatOpenAI
from MCP import mcp_config
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.Helpers.config import Settings

class OpenaiProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
        self._llm_with_tools = None
        self._llm = None
        self._tools = None

    def initialize_llm(self):
        self._llm = ChatOpenAI(api_key=self._settings.OPENAI_API_KEY,
                               model=self._settings.GENERATION_MODEL_ID,
                               temperature=self._settings.GENERATION_DAFAULT_TEMPERATURE)
        
        return None

    async def initialize_llm_mcptools(self, mcp_config: dict):
        client =  MultiServerMCPClient(connections=mcp_config["mcpServers"])
        tools = await client.get_tools()
        self._tools = tools
        self._llm_with_tools = ChatOpenAI(api_key=self._settings.OPENAI_API_KEY,
                                          temperature=self._settings.GENERATION_DAFAULT_TEMPERATURE,
                                          model=self._settings.GENERATION_MODEL_ID).bind_tools(tools=self._tools)

        return None
    
    @property
    def llm(self):
        if self._llm is None : 
            raise RuntimeError("LLM has not been initialized. Call 'initialize()' first.")
        return self._llm
    
    @property
    def llm_with_tools(self):
        if self._llm_with_tools is None:
            raise RuntimeError("LLM has not been initialized. Call 'initialize()' first.")
        return self._llm_with_tools

    @property
    def tools(self):   
        if self._tools is None:
            raise RuntimeError("Tools has not been initialized. Call 'initialize()' first.")
        return self._tools
