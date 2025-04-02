import json
import requests
from typing import Any
from ..utils.base_url import URL_BASE
from ..campus.get_campi import get_campi
from ..campus.utils import get_campus_most_similar
from langchain_ollama import ChatOllama
from ..utils.execute_sql import execute_sql
import re

from sentence_transformers import SentenceTransformer
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

prompt_sql_cursos = """
Você é um agente especialista em gerar comando SQL!

A seguinte tabela é dos cursos de graduação:

Curso (
    codigo_do_curso INTEGER -- Codigo do curso
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

<ATENÇÂO>
- Use operadores matemáticos do SQL se o usuário perguntar algo quantidicadores como MIN, MAX, COUNT, SUM, AVERAGE, dentre outros.
- Use a clausula WHERE se precisar. 
- Gere apenas UM comando SQL que reponda toda a pergunta.
</ATENÇÂO>

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

        #sql_sem_rag = response.content
        #sql_com_rag = atributos_mais_similar_tabela_curso(pergunta_feita)

        #TESTE SQL COM RAG!!!!
        #sql = atributos_mais_similar_tabela_curso(pergunta_feita)
        #sql = sql.lstrip('```sql\n').rstrip('```').strip()

        sql0 = teste_gerar_sql_diferentes_temperaturas(pergunta_feita=pergunta_feita, prompt=prompt_sql_cursos,temperatura=0)
        sql1 = teste_gerar_sql_diferentes_temperaturas(pergunta_feita=pergunta_feita,prompt=prompt_sql_cursos,temperatura=0.15)
        sql2 = teste_gerar_sql_diferentes_temperaturas(pergunta_feita=pergunta_feita,prompt=prompt_sql_cursos,temperatura=0.3)
        sql3 = teste_gerar_sql_diferentes_temperaturas(pergunta_feita=pergunta_feita,prompt=prompt_sql_cursos,temperatura=0.45)

        sql_rag0 = atributos_mais_similar_tabela_curso(pergunta=pergunta_feita, temperatura=0)
        sql_rag1 = atributos_mais_similar_tabela_curso(pergunta=pergunta_feita, temperatura=0.15)
        sql_rag2 = atributos_mais_similar_tabela_curso(pergunta=pergunta_feita, temperatura=0.3)
        sql_rag3 = atributos_mais_similar_tabela_curso(pergunta=pergunta_feita, temperatura=0.45)

        print("SQL COM T=0 ", sql0)
        print("SQL COM T=0.15 ", sql1)
        print("SQL COM T=0.30 ", sql2)
        print("SQL COM T=0.45 ", sql3)

        print()
        print("SQL COM RAG T = 0 ", sql_rag0)
        print("SQL COM RAG T = 1 ", sql_rag1)
        print("SQL COM RAG T = 2 ", sql_rag2)
        print("SQL COM RAG T = 3 ", sql_rag3)

        sql_melhor_sem_rag = escolhe_melhor_sql(pergunta_feita=pergunta_feita, sql0=sql0, sql1=sql1, sql2=sql2, sql3=sql3)
        sql_melhor_com_rag = escolhe_melhor_sql(pergunta_feita=pergunta_feita, sql0=sql_rag0, sql1=sql_rag1, sql2=sql_rag2, sql3=sql_rag3)

        print("SQL_MELHOT_SEM_RAG ", sql_melhor_sem_rag)
        print("SQL_MELHOR_COM_RAG ", sql_melhor_com_rag)

        
        sql  = escolhe_melhor_sql_dentre_dois(pergunta_feita=pergunta_feita, sql0 = sql_melhor_sem_rag, sql1 = sql_melhor_com_rag)
        
        print("SQL ESCOLHIDO= ",sql)
        #atributos_mais_similar_tabela_curso(pergunta=pergunta_feita)


        result = execute_sql(sql, db_name)
        print("RESSULTTT ", result)
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
        print("DADOOOOS ", dados)
        return dados
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]
    

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




attributes = """
nome_do_curso Text, -- Nome do curso;
codigo_do_setor INTEGER, --;
nome_do_setor Text, --;
campus INTEGER, -- Usar número inteiro se informar o campus em representação romana;
nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal";
turno Text, -- Turno do curso pode ser "Matutino", "Vespertino", "Noturno" e "Integral";
periodo_de_inicio REAL, -- período em que o curso foi criado/fundado;
data_de_funcionamento Text, -- Data em formato de Texto sobre quando o curso foi criado "YYYY-MM-DD" (usar esses zeros), deve converter em date;
codigo_inep INTEGER, -- ;
modalidade_academica" Text, -- Pode ser "BACHARELADO" ou "LICENCIATURA";
curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada;
ciclo_enade INTEGER -- De quantos em quantos semestres ocorre a prova do enade 
"""

def atributos_mais_similar_tabela_curso(pergunta: str, temperatura: float) -> list:
    atributos_split = [atributo.replace("_", " ") for atributo in attributes.split(";")]
    sentence_transformers = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings_pergunta = sentence_transformers.encode(pergunta).reshape(1, -1)
    embeddings_atributo = sentence_transformers.encode(atributos_split)
    similaridades = cosine_similarity(embeddings_pergunta, embeddings_atributo).flatten()
    top_indices = np.argsort(similaridades)[::-1]

    tops = [f"atributo: {atributos_split[idx].split('--')[0]} tem similaridade de {similaridades[idx]:.2f}" for idx in top_indices]

    for i in tops:
        print(i)

    model = ChatOllama(model="llama3.1", temperature=temperatura)
    response = model.invoke(f"""Sabendo que tenho essa tabela Curso\n {attributes} \n\n e esses atributos \n\n {tops} tem seus devidos nomes e probabilidades para responder a pergunta. \n\n Gere um comando SQL que responda a seguinte pergunta {pergunta}. Gere apenas o comando SQL que responda a pergunta e mais nada!""")
    print(response.content)

    return response.content

tabela = """
Curso (
    codigo_do_curso INTEGER -- Codigo do curso
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
"""

ESCOLHE_SQL_PROMPT = """
    Você é um assistente que recebe duas consultas SQL e deve decidir qual consulta está mais correta e qual
    responde melhor a pergunta "{pergunta_feita}".

    ***IMPORTANTE***
    - VOCÊ DEVE RETORNAR SOMENTE A CONSULTA ESCOLHIDA E MAIS NADA!.
    - Não modifique nenhuma das consultas.

    Primeira consulta: "{sql0}"
    Segunda consulta: "{sql1}"
    Terceira consulta: "{sql2}"
    Quarta consulta: "{sql3}"

    Tabela:
        "{tabela}"

"""

ESCOLHE_SQL_DENTRE_DOIS_PROMPT = """
    Você é um assistente que recebe duas consultas SQL e deve decidir qual consulta está mais correta e qual
    responde melhor a pergunta "{pergunta_feita}".

    ***IMPORTANTE***
    - VOCÊ DEVE RETORNAR SOMENTE A CONSULTA ESCOLHIDA E MAIS NADA!.
    - Não modifique nenhuma das consultas.

    Primeira consulta: "{sql0}"
    Segunda consulta: "{sql1}"
   
    Tabela:
        "{tabela}"

"""

def escolhe_melhor_sql(pergunta_feita:str, sql0: str, sql1 : str, sql2:str, sql3: str):
        
        model = ChatOllama(model="llama3.1", temperature=0)
        response = model.invoke(ESCOLHE_SQL_PROMPT.format(pergunta_feita=pergunta_feita, sql0=sql0, sql1=sql1, sql2=sql2, sql3=sql3, tabela=tabela))

        return response.content


def escolhe_melhor_sql_dentre_dois(pergunta_feita:str, sql0:str, sql1: str):

        model = ChatOllama(model="llama3.1", temperature=0)
        response = model.invoke(ESCOLHE_SQL_PROMPT.format(pergunta_feita=pergunta_feita, sql0=sql0, sql1=sql1, tabela=tabela))

        return response.content


def teste_gerar_sql_diferentes_temperaturas(pergunta_feita: str, prompt: str, temperatura: float):
        """
            Gera consultas SQL com a temperatura informada

            Args:
                pergunta_feita: pergunta feito pelo usuário
                prompt: prompt que será usado no modelo internamente na função
                temperatura: temperatura escolhida
            
            Returns:
                SQL para a pergunta gerado de acordo com a temperatura informada.
        """
        
        model = ChatOllama(model="llama3.1", temperature=temperatura)
        response = model.invoke(prompt.format(pergunta_feita=pergunta_feita))


        return response.content




