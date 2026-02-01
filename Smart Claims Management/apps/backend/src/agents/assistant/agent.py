from smolagents import CodeAgent, PythonInterpreterTool, FinalAnswerTool, OpenAIServerModel, ToolCall, FinalAnswerStep
import os, json

from agents.assistant.tools import load_client_data, issue_a_reimbursement, rag_call, modify_client_data
from agents.assistant.prompt import PROMPT
from dotenv import load_dotenv

load_dotenv()


class AssistantAgent:
    def __init__(self, model="gpt-5.1", max_steps=12):
        self.model = OpenAIServerModel(
            model_id=model,
            api_base="https://api.openai.com/v1",
            api_key=os.environ["OPENAI_API_KEY"]
        )

        self.tools = [load_client_data, issue_a_reimbursement, rag_call, modify_client_data,PythonInterpreterTool(), FinalAnswerTool()]

        self.agent = CodeAgent(tools=self.tools, model=self.model,
                               additional_authorized_imports=['pandas', "os", "numpy.*",
                                                              "csv", "json", "posixpath", "datetime"], max_steps=max_steps)

    def __call__(self, query=None, history=None, stream=False, session_id=None):
        prompt = PROMPT
        if session_id:
            prompt += f"Session ID : {session_id}\n\n"
        
        if history:
            prompt += f"     Current History of Conversation : {history}\n\n"
        if query:
            prompt += f"    User Question : {query}"

        if stream:
            return self._stream_generator(prompt)
        return self.agent.run(prompt, stream=False)

    def _stream_generator(self, prompt):
        for step in self.agent.run(prompt, stream=True):
            content, type_ = self.parse_step(step)
            if content:
                yield json.dumps({"type": type_, "content": content}) + "\n"

    def parse_step(self, step):
        if type(step) == ToolCall and step.name == "python_interpreter":
            print("happend")
            return f"\n```python\n{step.arguments}\n```\n\n", "code"
        elif type(step) == FinalAnswerStep:
            return f"{step.output}\n", "final"
        return "", "other"

if __name__ == "__main__":
    agent = AssistantAgent()
    print("--- Testing Assistant Agent ---")
    
    # 1. Summarize Case
    print("\n[User]: Summarize the case for client C12345 who sent an email about glasses.")
    response = agent("Summarize the case for client C12345 who sent an email about glasses.")
    print(f"[Agent]: {response}")

    # 2. Check Rules (RAG)
    print("\n[User]: What are the rules for optical reimbursement in Sante?")
    response = agent("What are the rules for optical reimbursement in Sante?")
    print(f"[Agent]: {response}")

    # 3. Draft Response
    print("\n[User]: Draft a response to the client saying we are checking it.")
    response = agent("Draft a response to the client saying we are checking it.")
    print(f"[Agent]: {response}")



