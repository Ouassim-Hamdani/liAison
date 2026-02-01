from enum import Enum

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

class Department(str, Enum):
    PREVOYANCE_INCAPACITE = "prevoyance_incapacite"
    PRESTATIONS_SANTE = "prestations_sante"
    GESTION_ADMINISTRATIVE = "gestion_administrative"
    COTISATIONS_ENTREPRISES = "cotisations_entreprises"
    EPARGNE_RETRAITE = "epargne_retraite"
    OTHER = "other"


class UrgencyLevel(str, Enum):
    LOW = "low"  # Standard information requests, status checks
    MEDIUM = "medium"  # Standard claims, reimbursements
    HIGH = "high"  # Urgent care, hospitalization pre-approval
    CRITICAL = "critical"  # Life-threatening situations, immediate assistance
    
class DispatcherResult(BaseModel):
    """Result of the dispatcher classification."""

    department: Department = Field(
        ...,
        description="The department best suited to handle the request.",
    )
    urgency: UrgencyLevel = Field(
        ..., description="The estimated urgency level of the request."
    )
    reasoning: str = Field(
        ..., description="Brief explanation of why this classification was chosen."
    )
