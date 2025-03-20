import json
import requests
from typing import Any
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from .utils import get_disciplina_grade_most_similar
from ..utils.base_url import URL_BASE
import sqlite3
from langchain_ollama import ChatOllama
import re

prompt_sql_disciplinas = """
Você é um agente especialista em gerar comando SQL!

A seguinte tabela é de EstudanteDisciplina:

EstudanteDisciplina (
matricula_do_estudante TEXT, -- Matrícula do estudante.
turma INTEGER, -- Número da turma da disciplina.
status TEXT, -- Situação do estudantes e que o Enum que pode ser "Aprovado", "Trancado", "Reprovado", "Reprovado por Falta".
media_final REAL, Nota do aluno na disciplina (sar se pedir informações de notas e médias).
dispensou TEXT -- Enum que pode ser "Sim" ou "Não".
)

<ATENÇÂO>
- Ignore o a discipliina, curso e o campus caso haja na pergunta (assuma que esses estudantes já são o esperado).
- Selecione apenas o atributo da tabela que o usuário perguntou para responder a pergunta na clausula WHERE.
- NÃO use atributos da tabela que o usuário não forneceu. Use apenas o que ele forneceu.
- Gere apenas o comando SQL e mais nada!
</ATENÇÂO>

Dado a tabela a acima, responda: 
"{pergunta_feita}"
"""

def get_notas_turma_disciplina(nome_da_disciplina: Any, nome_do_curso: Any, nome_do_campus: Any, pergunta_feita: Any, turma: Any = "01", periodo: Any = "") -> dict:
    """
    Busca as notas / desempenho dos estudantes em uma turma de uma disciplina.

    Args:
        nome_da_disciplina: nome da disciplina.
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (Se o usuário não informou o campus de Campina Grande)
        pergunta_feita: pergunta feita pelo usuário.
        turma: valor numérico da turma da disciplina (se não foi informada, então passe a strig vazia '').
        periodo: periodo do curso (se não foi informado, então passe a string vazia '').
    
    Returns:
        Informações relacionados aos estudantes da disciplina.
    """
    
    nome_da_disciplina=str(nome_da_disciplina)
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    pergunta_feita=str(pergunta_feita)
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
        
        model = ChatOllama(model="llama3.1", temperature=0)
        #model = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = prompt_sql_disciplinas.format(pergunta_feita=pergunta_feita)
        response = model.invoke(prompt)

        print(prompt)
        sql = response.content
        print(sql)

        result = execute_sql(sql, db_name=db_name)
        dados = [[] for _ in range(len(result))]

        match = re.search(r"SELECT (.*?) FROM", sql)
        if match:
            campos = [campo.strip() for campo in match.group(1).split(",")]
            for r in range(len(result)):
                for i in range(len(campos)):
                    if i < len(result[r]):
                        dados[r].append(f"{campos[i].strip()}: {result[r][i]}")
        
        return dados
    
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
    
def save_disciplinas(data_json, db_name):
    """Salva as disciplinas em um banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EstudanteDisciplina (
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
        print(disciplina["media_final"])
        cursor.execute("""
        INSERT OR IGNORE INTO EstudanteDisciplina (
            matricula_do_estudante, codigo_da_disciplina, nome_da_disciplina, periodo, turma, status, tipo, media_final, dispensou
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            disciplina["matricula_do_estudante"],
            disciplina["codigo_da_disciplina"],
            disciplina["nome_da_disciplina"],
            disciplina["periodo"],
            disciplina["turma"],
            disciplina["status"],
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
