import json, requests, sqlite3
from typing import Any
from langchain_ollama import ChatOllama
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub

from ..utils.base_url import URL_BASE
from ..utils.execute_sql import execute_sql
from ..campus.utils import get_campus_most_similar

import warnings
warnings.filterwarnings("ignore", message="LangSmithMissingAPIKeyWarning")


class StateSQL(TypedDict):
    query: str
    question: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

class LLMGenerateSQL:
    def __init__(self, model: str, prompt: str):
        self.llm = ChatOllama(model=model, temperature=0)
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

        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}


tabela = """
CREATE TABLE IF NOT EXISTS Curso (
    codigo_do_curso INTEGER, -- Codigo do curso (ID: chave primária)
    nome_do_curso Text, -- Nome do curso
    codigo_do_setor INTEGER, -- Código do setor ao qual o curso pertence
    nome_do_setor Text, -- Nome do setor ao qual o curso pertence
    nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal".
    turno Text, -- Turno do curso pode ser "Matutino", "Vespertino", "Noturno" e "Integral"
    periodo_de_inicio REAL, -- período em que o curso foi criado/fundado
    data_de_funcionamento Text, -- Data em formato de Texto sobre quando o curso foi criado "YYYY-MM-DD" (usar esses zeros), deve converter em date
    codigo_inep INTEGER, -- Código INEP do curso 
    modalidade_academica Text, -- Pode ser "BACHARELADO" ou "LICENCIATURA"
    curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada
    ciclo_enade INTEGER, -- De quantos em quantos semestres ocorre a prova do enade 
);
"""

prompt = '''
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - codigo_do_curso
  - nome_do_curso
  - codigo_do_setor
  - nome_do_setor
  - nome_do_campus
  - turno
  - periodo_de_inicio
  - data_de_funcionamento
  - codigo_inep
  - modalidade_academica
  - curriculo_atual
  - ciclo_enade
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
'''

def get_informacoes_cursos(query: Any, nome_do_campus: Any = "") -> list:
    """
    Use quando precisar de informações de cursos em geral envolvendo:
    Essa tool tem informações sobre o nome do curso, nome do campus, turno do curso, período do de inicio do curso, data de criação do curso, código inep, modalidade academica (grau do curso) e curriculo atual e enade.

    Args:
        query: pergunta feita pelo usuário.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''.

    Returns:
        Lista contendo valores com as informações pedidas pelo usuário.
    """
    query=str(query)
    nome_do_campus=str(nome_do_campus)
    print(f"Tool get_informacoes_cursos chamada com nome_do_campus={nome_do_campus}")    

    params = { 'status':'ATIVOS' }

    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]
    
    url_cursos = f'{URL_BASE}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        print(len(data_json))
        db_name = "db_cursos.sqlite"
        save_db(data_json=data_json, db_name=db_name)

        sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)
        result = sqlGenerateLLM.write_query(query=query, tabela=tabela)
        print(result)
        result = execute_sql(result['query'], db_name)
        return result
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]

def save_db(data_json, db_name):
    """Salva os cursos em um banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Curso (
        codigo_do_curso INTEGER PRIMARY KEY,
        nome_do_curso TEXT,
        grau_do_curso TEXT,
        codigo_do_setor INTEGER,
        nome_do_setor TEXT,
        campus INTEGER,
        nome_do_campus TEXT,
        turno TEXT,
        periodo_de_inicio REAL,
        data_de_funcionamento TEXT,
        codigo_inep INTEGER,
        modalidade_academica TEXT,
        curriculo_atual INTEGER,
        area_de_retencao INTEGER,
        ciclo_enade INTEGER
    )
    """)

    cursor.execute("DELETE FROM Curso")

    for curso in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO Curso VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            curso["codigo_do_curso"],
            curso["descricao"],
            curso["grau_do_curso"],
            curso["codigo_do_setor"],
            curso["nome_do_setor"],
            curso["campus"],
            curso["nome_do_campus"],
            curso["turno"],
            curso["periodo_de_inicio"],
            curso["data_de_funcionamento"].split(" ")[0] if curso["data_de_funcionamento"] else "00-00-0000",
            curso["codigo_inep"],
            curso["modalidade_academica"],
            curso["curriculo_atual"],
            curso["area_de_retencao"],
            curso['ciclo_enade']
        ))

    conn.commit()
    conn.close()