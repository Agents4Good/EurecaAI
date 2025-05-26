import requests
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from vanna.base import VannaBase

class MyCustomLLmVanna(VannaBase):
    def __init__(self, LLM, config: dict = None):
        config = config or {}

        temperature = config.get("temperature", 0.0)
        max_tokens = config.get("max_tokens", 500)
        model = config["model"]

        self.client = LLM(model=model, temperature=temperature, max_tokens=max_tokens)
    
    def system_message(self, message: str) -> any:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> any:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> any:
        return {"role": "assistant", "content": message}

    def generate_sql(self, question: str, **kwargs) -> str:
        # Use the super generate_sql
        sql = super().generate_sql(question, **kwargs)

        # Replace "\_" with "_"
        sql = sql.replace("\\_", "_")

        return sql
    
    def convert_prompt(self, prompt):
        converted = []
        for message in prompt:
            role = message["role"]
            content = message["content"]
            if role == "system":
                converted.append(SystemMessage(content=content))
            elif role == "user":
                converted.append(HumanMessage(content=content))
            elif role == "assistant":
                converted.append(AIMessage(content=content))
        return converted

    def submit_prompt(self, prompt, **kwargs) -> str:
        langchain_messages = self.convert_prompt(prompt)
        response = self.client.invoke(langchain_messages)

        # Retorna só o conteúdo
        return response.content if hasattr(response, "content") else str(response)