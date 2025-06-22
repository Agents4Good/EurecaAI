import re
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
    
    def write_query_state(self, query, tabela)-> StateSQL:
       
        self.prompt = self.prompt.format(
            dialect="sqlite",
            table_info=tabela,
            input=query
        )
       
        print(f"\nPrompt: {self.prompt}")
        print("\n=========================\n")
        structured_llm = self.llm.with_structured_output(StateSQL,  method="function_calling")
        result = structured_llm.invoke(self.prompt)

        print("RESULTADO: ", result)

        return {"query": result["query"], "question": result["question"]}
  
    def write_query(self, query, tabela)-> StateSQL:
        self.prompt = self.prompt.format(
            dialect="sqlite",
            table_info=tabela,
            input=query
        )
        
        sql_gerado = self.llm.invoke(self.prompt).content
        print("SQL GERADOOOOOOOOO: ", sql_gerado)
        match = re.search(r'SELECT\b[\s\S]*?(?:;)?(?=\s*(?:```|\n?\}|"\s*\}|\s*$))', sql_gerado, re.IGNORECASE)

        if match:
            sql = match.group()
            sql = re.sub(r'\\n|\n', ' ', sql)
            sql = re.sub(r'\s+', ' ', sql).strip()
            print("REGEX: ", sql)
            return {"query": sql}
        else:
            return {"query": "Erro para consultar os dados"}