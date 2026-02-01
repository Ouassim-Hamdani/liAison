from smolagents import tool
import json
import os
from core.DBHandler import VectorDBManager
from core.config import CATEGORIES
CLIENT_DB_PATH = "C:\\Projects\\Hack in saclay\\Smart Customer Service\\data\\clients.json"





@tool
def load_client_data() -> str:
    """
    Retrieves the currently authenticated user's personal file. 
    Use this tool FIRST for any questions about "my" contract, "my" coverage, "my" claims, or "my" personal details.
    
    Returns:
        JSON string containing:
        - Client profile (age, status, id)
        - List of active contracts (Health/Sante, Providence/Prevoyance, Savings/Epargne) with their specific Option/Level.
        - Recent claims history and reimbursement status.
    """
    # return dummy client info for simulation
    with open("C:\\Projects\\Hack in saclay\\SMART CUSTOMER SERVICE\\data\\client.json", "r") as f:
        client = json.load(f)
    return json.dumps(client, indent=4)


@tool
def rag_call(query: str, category: str) -> str:
    """
    Using Rag, Searches the company's internal knowledge base for general policy information, guarantee tables, and legal conditions.
    
    Args:
        query: Specific keywords or phrases to search for (e.g., "osteopathie reimbursement", "delai carence", "loi evin guarantees").    
        category: The specific domain to search within. MUST be one of:
            - 'sante': For medical expenses, optical (glasses/lenses), dental, audiology, hospitalization, medicine, wellness/osteopathy.
            - 'prevoyance': For death benefits (décès), disability (invalidité), incapacity/work stoppage (arrêt travail), and daily allowances (IJ).
            - 'epargne_retraite': For retirement savings plans (PER), visualizations, liquidation rules, and pension contributions.
    
    Returns:
        A string containing relevant excerpts from policy documents.
    """
    if category not in CATEGORIES:
        return f"Error: Category '{category}' is invalid. Allowed categories: {CATEGORIES}"
    
    db_manager = VectorDBManager()
    results = db_manager.query(collection_name=category, query_text=query)
    
    if not results:
        return "No relevant documents found. Try refining your query."
    
    # Compile results
    combined_content = "\n----------------------------\n\n-------------------------\n".join([f"Source: {doc.metadata.get('source', 'Unknown')} (Page {str(doc.metadata.get('page_numbers', 'Unknown'))})\nContent:\n{doc.page_content}" for doc in results])
    return f"Top relevant documents:\n{combined_content}"

@tool
def open_formal_request(request_type: str, details: str) -> str:
    """
    Initiates a formal process or ticket for the user. Use this when the user explicitly asks to perform an action that cannot be resolved by information retrieval alone.
    
    Args:
        request_type: The category of the request. Examples: 'claim_dispute', 'contract_modification', 'certificate_request', 'advisor_contact'.
        details: A summary of what the user wants or the specific issue.
        
    Returns:
        Confirmation message with a reference ID.
    """
    # Simulate opening a formal request
    return f"Formal request of type '{request_type}' has been opened with details: {details}"

