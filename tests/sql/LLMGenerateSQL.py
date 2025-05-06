from langchain_community.chat_models import ChatDeepInfra
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

class StateSQL(TypedDict):
    query: str
    question: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

class LLMGenerateSQL:
    def __init__(self, LLM, model: str, prompt: str):
        self.llm = LLM(model=model, temperature=0)
        query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
        dict(query_prompt_template)['messages'][0].prompt.template = prompt
        self.query_prompt_template = query_prompt_template
  
    def write_query(self, query, tabela):
        prompt = self.query_prompt_template.invoke({
            'dialect': "sqlite",
            'table_info': tabela,
            'top_k': 10,
            'input': query
        })

        
        print("PROMPT:", prompt.messages[0].content)

      
        prompt = prompt.messages[0].content
        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}