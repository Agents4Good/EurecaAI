from langchain_community.chat_models import ChatDeepInfra
from typing import Optional, TypedDict
from typing_extensions import Annotated
from langchain_ollama import ChatOllama
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

class StateSQL(TypedDict):
    query: str
    question: str
    result: str
    answer: str
    previous_state: Optional[str]


prompt = """
    Você é um assistente de SQL. Você selecionar quais atributos da tabela são úteis para responder a pergunta do usuário.

    tabela: {table_info}
   
    Você deve gerar escolher os atributos levando em consideração o estado anterior.
    {previous_state}
    - O estado anterior são os campos que são interessantes para a consulta que foram escolhidos anteriormente.

    - Você deve escolher atributos que respondam a pergunta do usuário.
    {input}

    - Você deve retornar os atributos que você escolheu e mais nada.
    - Você deve retornar os atributos em uma lista com o nome e o tipo do atributo, separados por vírgula.
     Exemplo:
        ["telefone TEXT"]
"""

prompt_gera_sql = """
    Você é um assistente de SQL. Você deve gerar uma consulta SQL para responder a pergunta do usuário.
    Você deve usar os atributos os seguintes atributos da tabela Estudante para gerar a consulta SQL:
    {atributtes}

    Você deve gerar uma consulta SQL para responder a pergunta do usuário.
    {input}
    - Você deve retornar a consulta SQL e mais nada.
"""



class FieldAtributtes(TypedDict):
    query: Annotated[list[str], ..., "Lista de atributos selecionados da tabela com o nome e o tipo do atributo, separados por vírgula."]

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

from .GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado

class LLMGenerateSQL:
    def __init__(self, LLM, model: str, prompt: str, prompt_gera_sql: str):
        self.llm = LLM(model=model, temperature=0)
        self.prompt = prompt
        self.prompt_gera_sql = prompt_gera_sql


    def split_em_blocos(self,lista, tamanho=5):
        return [lista[i:i + tamanho] for i in range(0, len(lista), tamanho)]
    
    def write_query(self, tabela, state: StateSQL):
        
        g = GerenciadorSQLAutomatizado(tabela, "estudantes.sqlite")
        campos = self.split_em_blocos(g._extract_campus_types_description());

        print("CAMPOS ", campos)
        print("===========================\n")
    
        # prompt_gera_sql = prompt_gera_sql.format(
        #     previous_state=state["previous_state"],
        #     input=state["question"],
        # )


        for lista_campos in campos:
            prompt_campos = ""
            for campo in lista_campos:
                prompt_campos += f"\t{campo}\n"

            prompt = self.prompt.format(
                table_info=prompt_campos,
                previous_state=state["previous_state"],
                input=state["question"],
            )

            print("PROMPT: ", prompt)
            print("==========================")

            structured_llm = self.llm.with_structured_output(FieldAtributtes)
            result = structured_llm.invoke(prompt)

            #result = self.llm.invoke(prompt)
            print("RESULTADO: ", result["query"])
            state["previous_state"] = result["query"]




        atributes = state["previous_state"]
        print("RESULTADO FINAL: ", atributes)
      
        prompt_gera_sql = self.prompt_gera_sql.format(
            input=state["question"],
            atributtes=atributes
        )

        print("PROMPT SQL: ", prompt_gera_sql)
        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt_gera_sql)
        print("RESULTADO SQL: ", result["query"])

        # #passar um for em todos os campos da tabela
        # result = self.llm.invoke(prompt)

        # structured_llm = self.llm.with_structured_output(QueryOutput)
        # result = structured_llm.invoke(prompt)
        # return {"query": result["query"]}
    


agent = LLMGenerateSQL(LLM=ChatOllama, model="qwen3:4b", prompt=prompt, prompt_gera_sql=prompt_gera_sql);
query = "Traga o email das estudantes femininas solteiras que nasceram no ano de 2005 do curso de ciência da computação?"

result = agent.write_query(tabela="Estudante", state={"question": query, "query": "", "result": "", "answer": "", "previous_state": None})

  