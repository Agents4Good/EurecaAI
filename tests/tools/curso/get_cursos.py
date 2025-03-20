import json
import requests
from typing import Any
from ..utils.base_url import URL_BASE
from ..campus.get_campi import get_campi
from ..campus.utils import get_campus_most_similar
from langchain_ollama import ChatOllama
import sqlite3
import re

prompt_sql_cursos = """
Você é um agente especialista em gerar comando SQL!

A seguinte tabela é dos cursos de graduação:

Curso (
    nome_do_curso Text, -- Nome do curso
    codigo_do_setor INTEGER,
    nome_do_setor Text,
    campus INTEGER, -- Usar número inteiro se informar o campus em representação romana
    nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal".
    turno Text, -- Turno do curso pode ser "Matutino", "Vespertino", "Noturno" e "Integral"
    periodo_de_inicio REAL, -- período em que o curso foi criado/fundado
    data_de_funcionamento Text, -- Data em formato de Texto sobre quando o curso foi criado "YYYY-MM-DD" (usar esses zeros), deve converter em date
    codigo_inep INTEGER,
    modalidade_academica" Text, -- Pode ser "BACHARELADO" ou "LICENCIATURA"
    curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada
    ciclo_enade INTEGER -- De quantos em quantos semestres ocorre a prova do enade 
)

Selecione o(s) atributo(s) necessários para responder a pergunta (descricao (nome) do curso seria obrigatório voce trazer). Só retorne tudo se o usuário pedir informações gerais.
Selecione tambem os atributos que voce escolheu para retornar no select e traga sempre o nome do curso no select.
Gere apenas o comando SQL e mais nada!

Dado a tabela a acima, responda:
"{pergunta_feita}"
"""

def get_cursos(pergunta_feita: Any, nome_do_campus: Any = "") -> list:
    """
    Use quando precisar de informações de curso(s) em geral envolvendo:
    Essa tool tem informações sobre o nome do curso, nome do campus, turno do curso, período do de inicio do curso, data de criação do curso, código inep, modalidade academica (grau do curso) e curriculo atual e enade.

    Args:
        pergunta_feita: pergunta feita pelo usuário.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''.

    Returns:
        Lista de cursos com 'codigo_do_curso' e 'descricao' que representa o nome e o turno do curso.
    """
    
    nome_do_campus=str(nome_do_campus)
    pergunta_feita=str(pergunta_feita)
    print(f"Tool get_cursos chamada com nome_do_campus={nome_do_campus}")
    
    params = {
        'status':'ATIVOS',
    }

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

        model = ChatOllama(model="llama3.1", temperature=0)
        response = model.invoke(prompt_sql_cursos.format(pergunta_feita=pergunta_feita))

        sql = response.content
        print(sql)
        result = execute_sql(sql, db_name)
        dados = [[] for _ in range(len(result))]

        match = re.search(r"SELECT (.*?) FROM", sql)
        if match:
            campos = [campo.strip() for campo in match.group(1).split(",")]
            for r in range(len(result)):
                for i in range(len(campos)):
                    if i < len(result[r]):
                        if campos[i].strip() == "ciclo_enade":
                            dados[r].append(f"{campos[i].strip()}: A cada {result[r][i]} períodos")
                        else:
                            dados[r].append(f"{campos[i].strip()}: {result[r][i]}")

        print(dados)
        return dados
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

def get_lista_cursos(nome_do_campus: Any = "") -> list:
    """
    Busca por todos os cursos da UFCG por campus, apenas o código do curos e o nome do curso.
    Usar apenas quando for perguntado sobre o código do curso.
    """
    
    nome_do_campus=str(nome_do_campus)
    print(f"Tool get_cursos chamada com nome_do_campus={nome_do_campus}")
    
    params = {
        'status-enum':'ATIVOS',
    }

    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]
    
    url_cursos = f'{URL_BASE}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'descricao': data['descricao']} for data in data_json]
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]