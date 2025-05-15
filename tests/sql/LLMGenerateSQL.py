from langchain_community.chat_models import ChatDeepInfra
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub
from dotenv import load_dotenv
load_dotenv()
import re

class StateSQL(TypedDict):
    query: str

# class QueryOutput(TypedDict):
#     query: Annotated[str, ..., "Syntactically valid SQL query."]

class LLMGenerateSQL:
    def __init__(self, LLM, model: str, prompt: str, temperature: float = 0):
        self.llm = LLM(model=model, temperature=temperature)
        self.prompt = prompt
  
    def write_query(self, question, tabela)-> StateSQL:
       
        self.prompt = self.prompt.format(
            dialect="sqlite",
            table_info=tabela,
            input=question
        )
       
        print(f"\nPrompt: {self.prompt}")
        print("\n=========================\n")
        structured_llm = self.llm.with_structured_output(StateSQL,  method="function_calling")
        result = structured_llm.invoke(self.prompt)

        return {"query": result["query"]}
    
    def write_query_state(self, question, tabela):
        self.prompt = self.prompt.format(
            dialect="sqlite",
            table_info=tabela,
            input=question
        )

        sql_gerado = self.llm.invoke(self.prompt).content
        return {"query": sql_gerado}