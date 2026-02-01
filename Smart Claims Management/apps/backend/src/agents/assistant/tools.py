from smolagents import tool
import json
import os
from core.DBHandler import VectorDBManager
from core.config import CATEGORIES
CLIENT_DB_PATH = "C:\\Projects\\Hack in saclay\\Repo\\data\\clients.json"

def _get_client_db():
    
    try:
        with open(CLIENT_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Helper to save DB
def _save_client_db(data):
    with open(CLIENT_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



@tool
def load_client_data(client_id: str) -> str:
    """
    Loads client details, contract information, and recent claims history.
    
    Args:
        client_id: The unique identifier of the client (e.g., 'C12345').
    """
    client_db = _get_client_db()
    client = client_db.get(client_id)
    if not client:
        return f"Client with ID {client_id} not found."
    return json.dumps(client, indent=2, ensure_ascii=False)


@tool
def issue_a_reimbursement(claim_id: str,client_id : str, amount: float) -> str:
    """
    Issues a reimbursement for a specific claim.
    
    Args:
        claim_id: The ID of the claim to reimburse.
        client_id: The unique identifier of the client.
        amount: The amount to reimburse in Euros.
    """
    # Simulation logic
    return f"SUCCESS: Reimbursement of {amount}€ for claim {claim_id} has been processed and sent to accounting."


@tool
def rag_call(query: str, category: str) -> str:
    """
    Searches internal company documents for specific policies or information.
    
    Args:
        query: The search query keywords.
        category: The category to search in. Must be either 'sante' or 'prevoyance' or 'epargne_retraite'.
    """
    if category not in CATEGORIES:
        return "Error: Category must be either 'sante' or 'prevoyance'."
    
    db_manager = VectorDBManager()
    results = db_manager.query(collection_name=category, query_text=query)
    
    if not results:
        return "No relevant documents found."
    
    # Compile results
    combined_content = "\n----------------------------\n\n-------------------------\n".join([f"Source: {doc.metadata.get('source', 'Unknown')} (Page {str(doc.metadata.get('page_numbers', 'Unknown'))})\nContent:\n{doc.page_content}" for doc in results])
    return f"Top relevant documents:\n{combined_content}"


@tool
def modify_client_data(client_id: str, field: str, value: str) -> str:
    """
    Updates a specific field in the client's record.
    
    Args:
        client_id: The unique identifier of the client.
        field: The field to update (e.g., 'address', 'phone', 'email').
        value: The new value for the field.
    """
    client_db = _get_client_db()
    client = client_db.get(client_id)
    if not client:
        return f"Client with ID {client_id} not found."
    
    if field not in client and field != "notes": 
         return f"Field '{field}' does not exist for this client. Available fields: {list(client.keys())}"
    
    old_value = client.get(field, "N/A")
    client[field] = value
    client_db[client_id] = client # Update db object
    _save_client_db(client_db) #
    return f"SUCCESS: Updated {field} for client {client_id}. Old value: '{old_value}' -> New value: '{value}'."
