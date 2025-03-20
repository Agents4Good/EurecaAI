import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..curso.utils import get_curso_most_similar
from ..campus.utils import get_campus_most_similar
from ..utils.base_url import URL_BASE
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import sqlite3
import re

prompt_sql_estudantes = """
Você é um agente especialista em gerar comando SQL!

A seguinte tabela é dos estudantes:

Estudante (
        nome_do_curso TEXT,
        turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
        codigo_do_curriculo INTEGER,
        nome_do_campus TEXT,
        estado_civil TEXT,
        sexo TEXT,
        forma_de_ingresso TEXT,
        nacionalidade TEXT,
        local_de_nascimento TEXT,
        naturalidade TEXT,
        cor TEXT,
        deficiencias TEXT,
        ano_de_conclusao_ensino_medio INTEGER,
        tipo_de_ensino_medio TEXT,
        politica_afirmativa TEXT,
        cra REAL,
        mc REAL,
        iea REAL,
        periodos_completados INTEGER,
        prac_atualizado TEXT,
        prac_renda_per_capita_ate REAL,
        prac_deficiente TEXT --ENUM que pode ser "Sim" ou "Não"
)

Selecione o(s) atributo(s) necessários para responder a pergunta. Só retorne tudo se o usuário pedir informações gerais.
Selecione tambem os atributos que voce escolheu para retornar no select.
Gere apenas o comando SQL e mais nada!

Dado a tabela a acima, responda:
"{pergunta_feita}"
"""

def get_estudantes(nome_do_curso: Any, nome_do_campus: Any, pergunta_feita: Any) -> dict:
    """
    Buscar informações gerais dos estudantes da UFCG com base no curso.

    Args:
        nome_do_curso: nome do curso (se quiser todos os estudantes da UFCG (de todas as universidades), use a string vazia '' para obter os estudantes de todos os cursos).
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser informações dos estudantes de todos os campus (toda a UFCG), passe a string vazia ''. 
        pergunta_feita: Perfeita feita pelo usuário.

    Returns:
        Dicionário com informações como 'sexo', 'nacionalidades', 'idade' (míninma, máxima, média), 'estados' (siglas), renda_per_capita (quantidade de salário mínimo) e assim por diante.
    """

    print(f"Tool get_estudantes chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")    
    
    params = { "situacao-do-estudante": "ATIVOS" }
    
    pergunta_feita = str(pergunta_feita)
    nome_do_campus = str(nome_do_campus)
    nome_do_curso = str(nome_do_curso)
    
    if (nome_do_curso != "" and nome_do_campus != ""):
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        params["curso"] = dados_curso['curso']['codigo']
    
    elif (nome_do_curso == "" and nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params["campus"] = dados_campus['campus']['codigo']
    
    elif (nome_do_curso == "" and nome_do_campus == ""):
        pass
    else:
        return [{"error_status": 500, "msg": "Não foi possível obter a informação porque você informou um curso sem passar o campus dele."}]
    
    response = requests.get(f'{URL_BASE}/estudantes', params=params)

    if response.status_code == 200:
        estudantes = json.loads(response.text)
        print(len(estudantes))
        db_name = "estudantes_db.sqlite"
        save_estudantes(estudantes, db_name)

        model = ChatOllama(model="llama3.1", temperature=0)
        #model = ChatOpenAI(model="gpt-4o", temperature=0)
        prompt = prompt_sql_estudantes.format(pergunta_feita=pergunta_feita)
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
    

def save_estudantes(data_json, db_name):
    """Salva os estudantes em um banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Estudante (
        nome_do_curso TEXT,
        turno_do_curso TEXT,
        codigo_do_curriculo INTEGER,
        nome_do_campus TEXT,
        estado_civil TEXT,
        sexo TEXT,
        situacao TEXT,
        motivo_de_evasao TEXT,
        periodo_de_evasao TEXT,
        forma_de_ingresso TEXT,
        periodo_de_ingresso TEXT,
        nacionalidade TEXT,
        local_de_nascimento TEXT,
        naturalidade TEXT,
        cor TEXT,
        ano_de_conclusao_ensino_medio INTEGER,
        tipo_de_ensino_medio TEXT,
        politica_afirmativa TEXT,
        cra REAL,
        mc REAL,
        iea REAL,
        periodos_completados INTEGER,
        prac_atualizado TEXT,
        prac_renda_per_capita_ate REAL,
        prac_deficiente TEXT
    )
    """)

    cursor.execute("DELETE FROM Estudante")

    for estudante in data_json:
        # Convertendo a lista de deficiências e deficiências no formato texto adequado

        cursor.execute("""
        INSERT OR IGNORE INTO Estudante (
            nome_do_curso, turno_do_curso, codigo_do_curriculo, nome_do_campus, estado_civil, sexo, situacao, 
            motivo_de_evasao, periodo_de_evasao, forma_de_ingresso, periodo_de_ingresso, nacionalidade, 
            local_de_nascimento, naturalidade, cor, ano_de_conclusao_ensino_medio, 
            tipo_de_ensino_medio, politica_afirmativa, cra, mc, iea, periodos_completados, 
            prac_atualizado, prac_renda_per_capita_ate, prac_deficiente
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            estudante["nome_do_curso"],
            estudante["turno_do_curso"],
            estudante["codigo_do_curriculo"],
            estudante["nome_do_campus"],
            estudante["estado_civil"],
            estudante["sexo"],
            estudante["situacao"],
            estudante["motivo_de_evasao"],
            estudante["periodo_de_evasao"],
            estudante["forma_de_ingresso"],
            estudante["periodo_de_ingresso"],
            estudante["nacionalidade"],
            estudante["local_de_nascimento"],
            estudante["naturalidade"],
            estudante["cor"],
            estudante["ano_de_conclusao_ensino_medio"],
            estudante["tipo_de_ensino_medio"],
            estudante["politica_afirmativa"],
            estudante["cra"],
            estudante["mc"],
            estudante["iea"],
            estudante["periodos_completados"],
            estudante["prac_atualizado"],
            estudante["prac_renda_per_capita_ate"],
            estudante["prac_deficiente"]
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
    