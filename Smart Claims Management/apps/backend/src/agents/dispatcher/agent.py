from agents.dispatcher.prompt import SYSTEM_PROMPT
from agents.dispatcher.classes import DispatcherResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()






class DispatcherAgent:
    """
    Agent responsible for dispatching insurance requests to the correct department
    and assessing urgency.
    """

    def __init__(self, model_name: str = "gpt-5.1", temperature: float = 0):
        self.model_name = model_name
        self.temperature = temperature
        self.chain = self._build_chain()

    def _build_chain(self):
        """
        Builds the LangChain processing chain.
        """
        # Initialize the model - assumes OPENAI_API_KEY is set in environment
        llm = ChatOpenAI(temperature=self.temperature, model=self.model_name)

        # Bind the structured output schema
        structured_llm = llm.with_structured_output(DispatcherResult)

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("human", "{input}"),
            ]
        )

        # Create the chain
        return prompt | structured_llm

    def invoke(self, request_text: str) -> DispatcherResult:
        """
        Analyze a text request and return the classification result.
        """
        return self.chain.invoke({"input": request_text})


if __name__ == "__main__":
    # Simple test if run directly
    test_inputs = [
        "Bonjour, je voudrais savoir si mes lunettes sont remboursées.",
        "Je suis en arrêt de travail depuis 3 mois et je n'ai pas reçu mes indemnités.",
        "URGENT: Mon fils est à l'hôpital, il faut une prise en charge immédiate !",
    ]

    print("--- Testing Dispatcher Agent ---")
    agent = DispatcherAgent()
    for txt in test_inputs:
        print(f"\nInput: {txt}")
        try:
            result = agent.invoke(txt)
            print(f"Output: {result}")
        except Exception as e:
            print(f"Error: {e}")
