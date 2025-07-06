import json
from langchain_core.messages import AIMessageChunk
from typing import AsyncGenerator, Any , Dict
from langgraph.graph import StateGraph 
from langgraph.types import Command
from src.Agent.State.crm_state import AgentState
from src.Agent.Graph.crm_graph import CRMGraph



class StreamResponseBuilder:

    def __init__(self , graph_input : AgentState , graph : CRMGraph , config : Dict):
        self.graph_input = graph_input
        self.graph = graph 
        self.config = config

    async def event_stream(self):
        # Stream graph execution
        async for chunk in self._stream_graph_responses(self.graph_input, self.graph, config=self.config):
            yield chunk

        thread_state = await self.graph.get_state(config=self.config)

        # Handle interrupts
        while thread_state.interrupts:
            for interrupt in thread_state.interrupts:
                interrupt_json_str = json.dumps(interrupt.value, indent=2, ensure_ascii=False)
                yield f"\n\n--- 🔔 Human Approval Required ---\n{interrupt_json_str}\n"

                # For production: here you may return the interrupt state to the frontend and pause
                # But for demo purposes, simulate auto-approval
                # In real case, save the interrupt and let the user act later (via another API call)

                action = "continue"  # Simulating human action
                data = None

                async for resumed_chunk in self._stream_graph_responses(
                    Command(resume={"action": action, "data": data}),
                    self.graph,
                    config=self.config
                ):
                    yield resumed_chunk

                thread_state = await self.graph.get_state(config=self.config)


    async def _stream_graph_responses(
            self,
            input: dict[str, Any],
            graph: StateGraph,
            **kwargs
            ) -> AsyncGenerator[str, None]:
        """Asynchronously stream the result of the graph run.

        Args:
            input: The input to the graph.
            graph: The compiled graph.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The final LLM or tool call response
        """
        async for message_chunk, metadata in graph.astream(
            input=input,
            stream_mode="messages",
            **kwargs
            ):
            if isinstance(message_chunk, AIMessageChunk):
                if message_chunk.response_metadata:
                    finish_reason = message_chunk.response_metadata.get("finish_reason", "")
                    if finish_reason == "tool_calls":
                        yield "\n\n"

                if message_chunk.tool_call_chunks:
                    tool_chunk = message_chunk.tool_call_chunks[0]

                    tool_name = tool_chunk.get("name", "")
                    args = tool_chunk.get("args", "")

                    if tool_name:
                        tool_call_str = f"\n\n< TOOL CALL: {tool_name} >\n\n"
                    if args:
                        tool_call_str = args

                    yield tool_call_str
                else:
                    yield message_chunk.content
                continue