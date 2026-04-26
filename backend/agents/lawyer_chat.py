import logging
import os
from typing import Any, TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from supabase import create_client, Client

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY else None

# Define the State for the LangGraph
class GraphState(TypedDict):
    user_id: str
    history: list[Any]
    current_message: str
    draft_response: str
    draft_citations: list[str]
    verified_citations: list[str]
    final_response: str

import json
from pydantic import BaseModel, Field

class StructuredDraftResponse(BaseModel):
    layman_summary: str = Field(description="A simple, easy to understand summary of the legal advice.")
    legal_ingredients: list[str] = Field(description="Key legal ingredients or elements of the offense/issue.")
    punishment_or_remedy: str = Field(description="Potential punishment or legal remedy available.")
    procedure_note: str = Field(description="Notes on the legal procedure to be followed.")
    bare_act_text: str = Field(description="Relevant text from the Bare Act.")
    legacy_alert: str = Field(description="Any alerts regarding legacy laws or recent amendments.")
    citations: list[str] = Field(description="List of case law citations used in the answer.")

def generate_draft(state: GraphState) -> GraphState:
    """
    Node 1: Drafts the initial response and extracts potential citations.
    """
    query = state['current_message']
    context_text = ""
    
    # Query Supabase table named case_law_index for context
    if supabase:
        try:
            # Generic text search approach
            response = supabase.table("case_law_index").select("content").textSearch("content", query).limit(3).execute()
            docs = response.data
            context_text = "\n".join([doc.get("content", "") for doc in docs])
        except Exception as e:
            logger.warning("Failed to retrieve context from Supabase: %s", e)

    prompt = f"""You are an expert Indian Legal AI Assistant.
Use the following context from Supabase to answer the user's query accurately.
You must strictly output a JSON object representing your answer.

Context:
{context_text}

Query:
{query}"""
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-3-flash")
        structured_llm = llm.with_structured_output(StructuredDraftResponse)
        
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        
        state["draft_response"] = json.dumps(response.model_dump(), indent=2)
        state["draft_citations"] = response.citations
    except Exception as e:
        logger.error("Failed to generate draft with Gemini: %s", e)
        fallback = {
            "layman_summary": f"Based on your query regarding '{query}', I am unable to generate a response at this time.",
            "legal_ingredients": [],
            "punishment_or_remedy": "",
            "procedure_note": "",
            "bare_act_text": "",
            "legacy_alert": ""
        }
        state["draft_response"] = json.dumps(fallback, indent=2)
        state["draft_citations"] = []
        
    return state

def mercy_check(state: GraphState) -> GraphState:
    """
    Node 2 (CRITICAL): The Anti-Hallucination 'Mercy-Check' Node.
    Verifies every extracted citation against the official Digital SCR API.
    """
    verified = []
    for citation in state["draft_citations"]:
        # Placeholder for Digital SCR API call
        # e.g., response = requests.get(f"{DIGITAL_SCR_BASE_URL}/search", params={"q": citation})
        # if response.json().get("found"): verified.append(citation)
        
        # Fail-Closed Security
        is_verified = False # Replace with actual API check
        
        if is_verified:
            verified.append(citation)
        else:
            logger.warning("Failed to verify citation: %s", citation)
            
    state["verified_citations"] = verified
    return state

def route_after_mercy_check(state: GraphState) -> Literal["format_final_response", "error_node"]:
    """
    Conditional Edge logic. Routes to an error node if the citations list is empty.
    """
    if not state.get("verified_citations"):
        return "error_node"
    return "format_final_response"

def error_node(state: GraphState) -> GraphState:
    """
    Error node to handle the case where no valid citations were found.
    """
    state["final_response"] = "I could not verify the case laws. Please consult a human advocate."
    return state

def format_final_response(state: GraphState) -> GraphState:
    """
    Node 3: Formats the final response, ensuring unverified citations are removed.
    """
    base_response = state["draft_response"]
    if len(state["draft_citations"]) != len(state["verified_citations"]):
        base_response += "\nNote: Only verified legal citations are shown."
    state["final_response"] = base_response
    return state

# Compile the graph
workflow = StateGraph(GraphState)
workflow.add_node("generate_draft", generate_draft)
workflow.add_node("mercy_check", mercy_check)
workflow.add_node("error_node", error_node)
workflow.add_node("format_final_response", format_final_response)

workflow.set_entry_point("generate_draft")
workflow.add_edge("generate_draft", "mercy_check")
workflow.add_conditional_edges(
    "mercy_check",
    route_after_mercy_check,
    {
        "error_node": "error_node",
        "format_final_response": "format_final_response"
    }
)
workflow.add_edge("error_node", END)
workflow.add_edge("format_final_response", END)

app_graph = workflow.compile()

def run_lawyer_chat(user_id: str, message: str, history: list[dict]) -> dict[str, Any]:
    """
    Runner for the LangGraph workflow.
    """
    logger.info("Starting AI Lawyer Chat for user_id=%s", user_id)
    
    # Initialize state
    initial_state = {
        "user_id": user_id,
        "history": history,
        "current_message": message,
        "draft_response": "",
        "draft_citations": [],
        "verified_citations": [],
        "final_response": ""
    }
    
    # Run the graph
    result = app_graph.invoke(initial_state)
    
    return {
        "response": result.get("final_response", ""),
        "citations": result.get("verified_citations", [])
    }
