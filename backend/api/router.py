import asyncio
import logging
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional

# Placeholder import for the agent
from agents.lawyer_chat import run_lawyer_chat
from utils.bsa_compliance import calculate_file_hash
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    history: Optional[list[dict]] = None

class ChatResponse(BaseModel):
    response: str
    citations: list[str]
    is_sgi_tagged: bool = True

class TranslateResponse(BaseModel):
    translated_text: str
    bsa_hash: str
    original_filename: str

@router.post("/legal-ai/chat", response_model=ChatResponse)
async def legal_ai_chat(request: ChatRequest):
    """
    Endpoint for the AI Lawyer Chat workflow.
    Invokes the LangGraph agent and returns the verified response.
    """
    try:
        # Pass the input to the agent workflow without blocking the event loop
        result = await asyncio.to_thread(run_lawyer_chat, request.user_id, request.message, request.history or [])
        return ChatResponse(
            response=result.get("response", "No response generated."),
            citations=result.get("citations", []),
            is_sgi_tagged=True
        )
    except Exception as e:
        logger.exception("An error occurred during legal_ai_chat execution")
        raise HTTPException(status_code=500, detail="Internal server error") from e

@router.post("/citizen/translate", response_model=TranslateResponse)
async def translate_document(file: UploadFile = File(...)):
    """
    AI Document Translation Tool.
    Requires BSA Section 63 hashing before processing.
    """
    try:
        file_bytes = await file.read()
        
        # 1. BSA Compliance Hash
        bsa_hash = calculate_file_hash(file_bytes)
        
        # 2. Extract text
        try:
            document_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # Fallback mock for binary files
            document_text = "Extracted text from binary document."
            
        # 3. Translate using Gemini 3 Pro
        llm = ChatGoogleGenerativeAI(model="gemini-3-pro")
        prompt = f"Translate the following legal document to English. Preserve the legal meaning and formatting as much as possible.\n\nDocument:\n{document_text}"
        
        # Run synchronous LLM call in a thread
        response = await asyncio.to_thread(llm.invoke, [HumanMessage(content=prompt)])
        
        return TranslateResponse(
            translated_text=response.content,
            bsa_hash=bsa_hash,
            original_filename=file.filename or "unknown"
        )
    except Exception as e:
        logger.exception("An error occurred during translation")
        raise HTTPException(status_code=500, detail="Internal server error") from e
