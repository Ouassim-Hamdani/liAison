from smolagents import CodeAgent, OpenAIServerModel, PythonInterpreterTool, FinalAnswerTool
import os
import json
from dotenv import load_dotenv

from agents.validator.prompt import VALIDATOR_PROMPT
from agents.assistant.tools import rag_call


load_dotenv()


class ValidatorAgent:
    def __init__(self, model="gpt-5.1", max_steps=10):
        self.model = OpenAIServerModel(
            model_id=model,
            api_base="https://api.openai.com/v1",
            api_key=os.environ["OPENAI_API_KEY"]
        )
        
        # We only need the RAG tool and FinalAnswer
        self.tools = [rag_call,PythonInterpreterTool(), FinalAnswerTool()] 

        self.agent = CodeAgent(
            tools=self.tools, 
            model=self.model,
            additional_authorized_imports=['json'],
            max_steps=max_steps
        )

    def validate(self, client_request: str, client_context: str, draft_response: str) -> str:
        """
        Validates a draft response.
        """
        # Construct the query/prompt for this specific validation instance
        query = (
            f"Please validate the following draft response.\n\n"
            f"--- CLIENT REQUEST ---\n{client_request}\n\n"
            f"--- CLIENT CONTEXT ---\n{client_context}\n\n"
            f"--- DRAFT RESPONSE ---\n{draft_response}\n\n"
            f"Perform the verification steps."
        )
        
        # We prepend the system prompt instructions to the run
        full_instruction = VALIDATOR_PROMPT + "\n\n" + query
        
        return self.agent.run(full_instruction)


if __name__ == "__main__":
    # Test the validator
    agent = ValidatorAgent()
    
    req = "Bonjour, je voudrais savoir si mes lunettes sont remboursées. J'ai une ordonnance de 2024."
    ctx = "Client: Jean Dupont. Contract: Sante. Claims: None."
    draft = "Bonjour Mr Dupont, Oui vos lunettes sont remboursées à 100% sans plafond. Cordialement."
    
    print("--- Testing Validator Agent ---")
    print("\nValidating Draft: ", draft)
    
    res = agent.validate(req, ctx, draft)
    print("\n[Validator Output]:\n", res)
