import asyncio
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Placeholder import for the agent
from agents.lawyer_chat import run_lawyer_chat

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str
    citations: List[str]
    is_sgi_tagged: bool = True

@router.post("/legal-ai/chat", response_model=ChatResponse)
async def legal_ai_chat(request: ChatRequest):
    """
    Endpoint for the AI Lawyer Chat workflow.
    Invokes the LangGraph agent and returns the verified response.
    """
    try:
        # Pass the input to the agent workflow without blocking the event loop
        result = await asyncio.to_thread(run_lawyer_chat, request.message, request.history or [])
        return ChatResponse(
            response=result.get("response", "No response generated."),
            citations=result.get("citations", []),
            is_sgi_tagged=True
        )
    except Exception as e:
        logger.exception("An error occurred during legal_ai_chat execution")
        raise HTTPException(status_code=500, detail="Internal server error") from e
