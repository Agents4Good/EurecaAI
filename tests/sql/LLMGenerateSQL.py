from langchain_community.chat_models import ChatDeepInfra
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

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

       
        structured_llm = self.llm.with_structured_output(StateSQL)
        sql_gerado = structured_llm.invoke(self.prompt)

        print("SQL GERADO ", sql_gerado["query"])
        return {"query": sql_gerado["query"]}