from smolagents import tool
import json
import os
from core.DBHandler import VectorDBManager
from core.config import CATEGORIES

COMPANY_DB_PATH = "c:\\Projects\\Hack in saclay\\Smart Company Service\\data\\company.json"

@tool
def load_company_data() -> str:
    """
    Retrieves the authenticated company's data.
    Use this to get the company contract details, list of attached employees, and contribution (cotisation) status.
    
    Returns:
        JSON string containing:
        - Company details (ID, Name)
        - Contracts list (Health, Providence, etc.)
        - List of employees (ID, Name, Position)
        - Cotisation status
    """
    try:
        with open(COMPANY_DB_PATH, "r") as f:
            company = json.load(f)
        return json.dumps(company, indent=4)
    except FileNotFoundError:
         return "Error: Company data file not found."

@tool
def get_employee_data(employee_name_or_id: str) -> str:
    """
    Retrieves detailed data for a specific employee.
    Use this when the HR asks about a specific employee's coverage, claims history, or status.
    
    Args:
        employee_name_or_id: The Name or Employee ID to search for.
        
    Returns:
        JSON string with employee details or an error message if not found.
    """
    try:
        with open(COMPANY_DB_PATH, "r") as f:
            company = json.load(f)
        
        employees = company.get("employees", [])
        for emp in employees:
            if emp["employee_id"] == employee_name_or_id or emp["name"] == employee_name_or_id:
                return json.dumps(emp, indent=4)
        
        return f"Employee '{employee_name_or_id}' not found in the company registry."
    except Exception as e:
        return f"Error retrieving employee data: {str(e)}"

@tool
def send_official_claim(employee_id: str, claim_type: str, details: str) -> str:
    """
    Sends an official claim or declaration on behalf of an employee or the company.
    Use this for filing claims, reporting work stoppages, or official requests.
    
    Args:
        employee_id: The ID of the employee concerned (or 'COMPANY' if it's a company-wide claim).
        claim_type: Type of claim (e.g., 'Work_Accident', 'Disability_Claim', 'Contract_Adjustment').
        details: Detailed description of the event or request.
        
    Returns:
        Confirmation message with a reference ID.
    """
    # Simulate API call to backend
    return f"✅ Official claim registered for {employee_id}. Type: {claim_type}. Reference: REF-{hash(details) % 10000}"

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

@tool
def list_employees() -> str:
    """
    Lists all employees attached to the authenticated company.
    
    Returns:
        JSON string containing a list of employees with their IDs and Names.
    """
    try:
        with open(COMPANY_DB_PATH, "r") as f:
            company = json.load(f)
        
        employees = company.get("employees", [])
        employee_list = [{"employee_id": emp["employee_id"], "name": emp["name"]} for emp in employees]
        return json.dumps(employee_list, indent=4)
    except Exception as e:
        return f"Error retrieving employee list: {str(e)}"