from langchain_community.chat_models import ChatDeepInfra
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

class StateSQL(TypedDict):
    query: str
    question: str

# class QueryOutput(TypedDict):
#     query: Annotated[str, ..., "Syntactically valid SQL query."]

class LLMGenerateSQL:
    def __init__(self, LLM, model: str, prompt: str, temperature: float = 0):
        self.llm = LLM(model=model, temperature=temperature)
        self.prompt = prompt
  
    def write_query(self, query, tabela)-> StateSQL:
        self.prompt = self.prompt.format(
            dialect="sqlite",
            table_info=tabela,
            input=query
        )

        sql_gerado = self.llm.invoke(self.prompt).content
        return {"query": sql_gerado}