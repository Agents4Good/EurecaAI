import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
import sqlite3
from langchain_ollama import ChatOllama
import re
from faker import Faker
faker = Faker('pt_BR')

from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub
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
CREATE TABLE IF NOT EXISTS EstudanteDisciplina (
    nome_do_estudante TEXT, -- nome do estudante (nome de pessoa).
    matricula_do_estudante TEXT, -- Número de 9 digitos que representa o número da matrícula do estudante (usar se informou a matrícula do estudante).
    status TEXT, -- É um ENUM que representa a situação do estudante na disciplina. O ENUM pode ser "Aprovado", "Trancado", "Reprovado por Nota", "Reprovado por Falta". E quando peguntar apenas uma palavra próximo a reprovação sem especificar se foi por nota ou por falta use "Reprovado por Nota" OR Reprovado por Falta".
    media_final REAL, -- Nota do aluno na disciplina (usar se pedir informações de notas e médias).
    dispensou TEXT -- ENUM que pode ser "Sim" ou "Não". (usar se perguntar sobre dispensas).
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
  - nome_do_estudante
  - matricula_do_estudante
  - status
  - media_final
  - dispensou
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
'''

def get_informacoes_aluno_disciplina(query: Any, nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, turma: Any = "01", periodo: Any = "") -> list:
    """
    Buscar informações relevantes dos estudantes em uma disciplina específica, como as matrículas deles, as notas (médias), dispensa da disciplina e o status (situação) dos estudantes na disciplina.

    Args:
        query: pergunta feita pelo usuário.
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Se o usuário não informou o campus de Campina Grande)
        turma: valor numérico da turma da disciplina (se não foi informada, então passe a strig vazia '').
        periodo: periodo do curso (se não foi informado, então passe a string vazia '').
    
    Returns:
        Informações relacionados aos estudantes da disciplina.
    """
    query=str(query)
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    
    turma=str(turma)
    periodo=str(periodo)
    curriculo= ""
    curriculo=str(curriculo)
    
    print(f"Tool get_media_notas_turma_disciplina chamada com nome_da_disciplina={nome_da_disciplina}, nome_do_curso={nome_do_curso}, nome_do_campus={nome_do_campus}, turma={turma}, periodo={periodo} e curriculo={curriculo}")
    dados_disciplina, _ = get_disciplina_grade_most_similar(nome_da_disciplina=nome_da_disciplina, nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus, curriculo=curriculo)
    
    if (periodo == ""):
        periodo = get_periodo_mais_recente()
    
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": dados_disciplina["disciplina"]["codigo"],
        "turma": turma
    }

    response = requests.get(f'{URL_BASE}/matriculas', params=params)

    if response.status_code == 200:
        matriculas = json.loads(response.text)
        db_name  ="db_disciplina.sqlite"
        save_disciplinas(matriculas, db_name)

        sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)
        result = sqlGenerateLLM.write_query(query=query, tabela=tabela)
        print(result)
        result = execute_sql(result['query'], db_name)
        return result
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]

def save_disciplinas(data_json, db_name):
    """Salva as disciplinas em um banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EstudanteDisciplina (
        nome_do_estudante TEXT,
        matricula_do_estudante TEXT,
        codigo_da_disciplina INTEGER,
        nome_da_disciplina TEXT,
        periodo TEXT,
        turma INTEGER,
        status TEXT,
        tipo TEXT,
        media_final REAL,
        dispensou TEXT
    )
    """)

    cursor.execute("DELETE FROM EstudanteDisciplina")

    for disciplina in data_json:
        Faker.seed(int(disciplina["matricula_do_estudante"]))
        print(disciplina["media_final"])
        cursor.execute("""
        INSERT OR IGNORE INTO EstudanteDisciplina (
            nome_do_estudante, matricula_do_estudante, codigo_da_disciplina, nome_da_disciplina, periodo, turma, status, tipo, media_final, dispensou
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            faker.name(),
            disciplina["matricula_do_estudante"],
            disciplina["codigo_da_disciplina"],
            disciplina["nome_da_disciplina"],
            disciplina["periodo"],
            disciplina["turma"],
            "Reprovado por Nota" if disciplina["status"] == "Reprovado" else disciplina["status"],
            disciplina["tipo"],
            disciplina["media_final"] if type(disciplina["media_final"]) == float else 0,
            "Sim" if (disciplina["dispensas"] and len(disciplina["dispensas"] > 0)) else "Não"
        ))

    conn.commit()
    conn.close()


def execute_sql(sql: str, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        conn.close()
        return [{"error": str(e)}]