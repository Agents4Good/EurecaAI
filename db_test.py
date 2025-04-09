from langchain_ollama import ChatOllama
from typing import TypedDict
from typing_extensions import Annotated
from langchain_community.utilities import SQLDatabase
from langchain import hub
import sqlite3

tabela = """
CREATE TABLE IF NOT EXISTS Estudante (
    nome_do_estudante TEXT, -- nome do estudante (usar nome em maiúsculo)
    matricula_do_estudante TEXT, -- Matrícula do estudante (usar se informou a matrícula do estudante).
    status TEXT, -- Situação do estudantes e que o Enum que pode ser "Aprovado", "Trancado", "Reprovado por Nota", "Reprovado por Falta". E quando peguntar apenas uma palavra próximo a reprovação sem especificar se foi por nota ou por falta use "Reprovado por Nota" OR Reprovado por Falta".
    media_final REAL, -- Nota do aluno na disciplina (usar se pedir informações de notas e médias).
    dispensou TEXT -- Enum que pode ser "Sim" ou "Não". (usar se perguntar sobre dispensas).
)
"""

def db_conn():
    conn = sqlite3.connect('Chinook.db')
    cursor = conn.cursor()
    cursor.execute(f"""{tabela}""")
    conn.commit()
    conn.close()

db_conn()

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

print(dict(query_prompt_template)['messages'][0].prompt.template)

dict(query_prompt_template)['messages'][0].prompt.template = '''
Essa tabela é da disciplina chamada "TEORIA DA COMPUTAÇÃO - D" do cuso de "CIENCIA DA COMPUTAÇÃO - INTEGRAL".
Dada uma pergunta de entrada, crie uma consulta {dialect} sintaticamente correta para executar e ajudar a encontrar a resposta.
- Nunca consulte todas as colunas de uma tabela específica, solicite apenas as poucas colunas relevantes para a pergunta.
- Preste atenção para usar apenas os nomes das colunas que você pode ver na descrição do esquema. Tome cuidado para não consultar colunas que não existem. 
- Faça o mais simples possível, ignorando o que partes que você não entender em como a pergunta se relaciona com os atributos (raciocine nessa parte).
- IMPORTANTE: NÃO USE LIKE!
Use apenas a seguintes tabela a seguir:

{table_info}

Raciocine observando atentamente!
'''

class StateSQL(TypedDict):
    query: str
    question: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

class SQL_Query_ByLLM:
    def __init__(self, model: str, prompt: str):
        self.llm = ChatOllama(model=model, temperature=0)
        self.prompt_db = prompt

    def write_query(self, query):
        state = StateSQL(query=query, question=query, result="", answer="")

        prompt = query_prompt_template.invoke({
            'dialect': db.dialect,
            'table_info': tabela,
            'top_k': 10,
            'input': state['question']
        })

        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}

prompt = """Gere um comando SQL que responda a seguinte pergunta"""
sql_query_llm = SQL_Query_ByLLM(model="llama3.1", prompt=prompt)

queries = [
    '''Quero o nome do estudante que tem a maior nota na turma 1 de ciencia da computação?''',
    '''Qual é a quantidade de estudantes na turma 1 de Teoria da Computação em ciencia da computação?''',
    '''Quantos estudantes existem na turma 1?''',
    '''Qual foi a nota de Matheus Hensley de Figueiredo e Silva?'''
    '''Qual foi a nota de Matheus Hensley de Figueiredo e Silva e de Levi de Lima Pereira Júnior?''',
    '''Quantos estudantes passaram na disciplina de teoria dos grafos?''',
    '''Quantos alunos dispensaram a disciplina de Fundamentos Matemáticos 2?'''
]

for query in queries:
    print(sql_query_llm.write_query(query=query))
