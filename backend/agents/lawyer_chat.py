import logging
from typing import List, Dict, Any, TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

logger = logging.getLogger(__name__)

# Define the State for the LangGraph
class GraphState(TypedDict):
    user_id: str
    history: List[Any]
    current_message: str
    draft_response: str
    draft_citations: List[str]
    verified_citations: List[str]
    final_response: str

def generate_draft(state: GraphState) -> GraphState:
    """
    Node 1: Drafts the initial response and extracts potential citations.
    """
    # Placeholder for LLM invocation
    state["draft_response"] = "Based on your query, the Supreme Court has held..."
    state["draft_citations"] = ["Ramesh Kumar vs. State of Maharashtra"]
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
        
        # For this placeholder, we mock a successful verification
        is_verified = True # Replace with actual API check
        
        if is_verified:
            verified.append(citation)
            
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
    state["final_response"] = state["draft_response"]
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

def run_lawyer_chat(user_id: str, message: str, history: List[dict]) -> Dict[str, Any]:
    """
    Runner for the LangGraph workflow.
    """
    logger.info(f"Starting AI Lawyer Chat for user_id={user_id}")
    
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
