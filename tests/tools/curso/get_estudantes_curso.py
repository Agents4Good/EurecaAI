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
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

prompt_sql_estudantes = """
Você é um agente especialista em gerar comando SQL!

A seguinte tabela é dos estudantes:

Estudante (
matricula_do_estudante TEXT,
turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
nacionalidade TEXT, ENUM que pode ser "Brasileira" ou "Estrangeira".
local_de_nascimento TEXT, Nome da cidade onde nasceu.
naturalidade TEXT, -- Sigla do estado do estudante.
cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
ano_de_conclusao_ensino_medio INTEGER, 
tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
cra REAL, -- Coeficiente de rendimento acadêmico.
mc REAL, -- Média de conclusão de curso.
iea REAL, --Indice de eficiência acadêmica.
periodos_completados INTEGER, 
prac_renda_per_capita_ate REAL
)

<ATENÇÂO>
- Ignore o curso e o campus caso haja na pergunta (assuma que esses alunos já são o esperado).
- Selecione apenas o atributo que o usuário perguntou para responder a pergunta na clausula WHERE.
- NÃO use atributos da tabela que o usuários não forneceu. Use apenas o que ele forneceu.
- Geralmente voce vai usar operadores SQL.
- Se selecionar atributos para o SQL não traga tudo 
- Gere apenas o comando SQL e mais nada!
</ATENÇÂO>

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
        Dicionário com informações como 'sexo', 'nacionalidades', 'idade' (míninma, máxima, média), 'estados' (siglas), renda_per_capita (quantidade de salário mínimo), tipo de escola, e assim por diante.
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

        dados = [[] for _ in range(len(estudantes))]

        # sql = response.content
        # print(sql)
        #atributos_mais_similar_tabela_estudante(pergunta=pergunta_feita)


        sql0 = teste_gerar_sql_diferentes_temperaturas(pergunta_feita=pergunta_feita, prompt=prompt_sql_estudantes,temperatura=0)
        sql1 = teste_gerar_sql_diferentes_temperaturas(pergunta_feita=pergunta_feita,prompt=prompt_sql_estudantes,temperatura=0.15)
       
        sql_rag0 = atributos_mais_similar_tabela_estudante(pergunta=pergunta_feita, temperatura=0)
        sql_rag1 = atributos_mais_similar_tabela_estudante(pergunta=pergunta_feita, temperatura=0.15)


        print("SQL COM T=0 ", sql0)
        print("SQL COM T=0.15 ", sql1)
        
        print()
        print("SQL COM RAG T = 0 ", sql_rag0)
        print("SQL COM RAG T = 0.15 ", sql_rag1)
        

        sql  = escolhe_melhor_sql(pergunta_feita=pergunta_feita, sql0=sql0, sql1=sql1, sql2=sql_rag0, sql3=sql_rag1)
       
        
        print("SQL ESCOLHIDO= ",sql)

        return

        selects = re.findall(r'SELECT.*?;', sql)

        resultado = []
        for select in selects:

            result = execute_sql(select, db_name=db_name)
            dados = [[] for _ in range(len(result))]

            match = re.search(r"SELECT (.*?) FROM", select)
            if match:
                campos = [campo.strip() for campo in match.group(1).split(",")]
                for r in range(len(result)):
                    for i in range(len(campos)):
                        if i < len(result[r]):
                            dados[r].append(f"{campos[i].strip()}: {result[r][i]}")
            
            resultado.append(f"sql={sql} resultado={dados}")
        
        return resultado

    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
    

def save_estudantes(data_json, db_name):
    """Salva os estudantes em um banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Estudante (
        matricula_do_estudante TEXT,
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
        deficiente TEXT
    )
    """)

    cursor.execute("DELETE FROM Estudante")

    for estudante in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO Estudante (
            matricula_do_estudante, nome_do_curso, turno_do_curso, codigo_do_curriculo, nome_do_campus, estado_civil, sexo, situacao, 
            motivo_de_evasao, periodo_de_evasao, forma_de_ingresso, periodo_de_ingresso, nacionalidade, 
            local_de_nascimento, naturalidade, cor, ano_de_conclusao_ensino_medio, 
            tipo_de_ensino_medio, politica_afirmativa, cra, mc, iea, periodos_completados, 
            prac_atualizado, prac_renda_per_capita_ate, deficiente
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            estudante["matricula_do_estudante"],
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
            "Sim" if len(estudante["deficiencias"]) > 0 else "Não"
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

attributes = """
matricula_do_estudante TEXT,
turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
nacionalidade TEXT, ENUM que pode ser "Brasileira" ou "Estrangeira".
local_de_nascimento TEXT, Nome da cidade onde nasceu.
naturalidade TEXT, -- Sigla do estado do estudante.
cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
ano_de_conclusao_ensino_medio INTEGER, 
tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
cra REAL, -- Coeficiente de rendimento acadêmico.
mc REAL, -- Média de conclusão de curso.
iea REAL, --Indice de eficiência acadêmica.
periodos_completados INTEGER, 
prac_renda_per_capita_ate REAL
"""

def atributos_mais_similar_tabela_estudante(pergunta: str, temperatura: float):
    atributos_split = [atributo.replace("_", " ") for atributo in attributes.split(";")]
    sentence_transformers = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings_pergunta = sentence_transformers.encode(pergunta).reshape(1, -1)
    embeddings_atributo = sentence_transformers.encode(atributos_split)
    similaridades = cosine_similarity(embeddings_pergunta, embeddings_atributo).flatten()
    top_indices = np.argsort(similaridades)[::-1]

    tops = [f"atributo: {atributos_split[idx].split('--')[0]} tem similaridade de {similaridades[idx]:.2f}" for idx in top_indices]

    # for i in tops:
    #     print(i)

    model = ChatOllama(model="llama3.1", temperature=temperatura)
    response = model.invoke(f"""Sabendo que tenho essa tabela n\n {attributes} \n\n e esses atributos \n\n {tops} tem seus devidos nomes e probabilidades para responder a pergunta. \n\n Gere um comando SQL que responda a seguinte pergunta {pergunta}. Gere apenas o comando SQL que responda a pergunta e mais nada!""")


    return response.content



tabela = """
Estudante (
matricula_do_estudante TEXT,
turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
nacionalidade TEXT, ENUM que pode ser "Brasileira" ou "Estrangeira".
local_de_nascimento TEXT, Nome da cidade onde nasceu.
naturalidade TEXT, -- Sigla do estado do estudante.
cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
ano_de_conclusao_ensino_medio INTEGER, 
tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
cra REAL, -- Coeficiente de rendimento acadêmico.
mc REAL, -- Média de conclusão de curso.
iea REAL, --Indice de eficiência acadêmica.
periodos_completados INTEGER, 
prac_renda_per_capita_ate REAL
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





