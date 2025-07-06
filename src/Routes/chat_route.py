from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from src.Routes.ChatSchemes.chat_request import ChatRequest
from src.Agent.Graph.crm_graph import CRMGraph
from src.Agent.State.crm_state import AgentState
from src.Routes.ChatSchemes.stream_response_builder import StreamResponseBuilder


router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/invoke")
async def invoke_chat(chat_request: ChatRequest):
    thread_id = chat_request.thread_id
    meesage_input = chat_request.message
    yolo_mode = chat_request.yolo_mode

    config = {
            "configurable": {
                "thread_id": thread_id
            }
        }
    
    graph_input = AgentState(
            messages=[
                HumanMessage(content=meesage_input)
            ],
            yolo_mode=yolo_mode
        )
    
    crm_graph = CRMGraph()
    graph = await crm_graph.get_graph()
    stream_response_builder = StreamResponseBuilder(graph_input=graph_input , 
                                                    graph=graph,
                                                    config=config)
    return StreamingResponse(stream_response_builder.event_stream(), media_type="text/plain")
