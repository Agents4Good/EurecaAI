from .prompts.prompts import *
from .agent.agent_tools import AgentTools
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from .tools.curso.get_curso import get_curso
#from .tools.curso.get_cursos import get_cursos
from .tools.curso.get_cursos import get_cursos
from .tools.curso.get_estudantes_curso import get_estudantes

tools = [
    get_curso,
    get_estudantes,
    get_cursos
]

"""
codigo_do_curso INTEGER,
    descricao Text, -- Nome do curso
    codigo_do_setor INTEGER,
    nome_do_setor Text,
    campus INTEGER, -- Usar número inteiro se informar o campus em representação romana
    nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal".
    turno Text, -- Turno do curso pode ser "MATUTINO", "VESPERTINO" E "NOTURNO"
    periodo_de_inicio REAL, -- período em que o curso foi criado/fundado
    data_de_funcionamento Text, -- Date em formato de Texto que indica a data quando o curso foi criado YYYY-MM-DD HH:MM:SS.0 (usar horas, minutos e segundos como 0)
    codigo_inep INTEGER,
    modalidade_academica" Text, -- Pode ser "BACHARELADO" ou "LICENCIATURA"
    curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada
    ciclo_enade INTEGER -- De quantos em quantos períodos ocorre a prova do enade
"""

#agent = AgentTools(LLM=ChatOpenAI, model="gpt-4o", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)
agent = AgentTools(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)

#question = "quais cursos da ufcg são de bacharelado curriculo?"
#question = "quais são os cursos que tiveram o currículo renovado a partir de 2010?"
#question = "Quantos cursos existem no campus de campina grande?"
#question = "Qual é o código do curso de ciencia da computação?"
#question = "Me fale quais foram os cursos que foram criados desde 2010"
#question = "Quais são os cursos de gaduacao do campus de sume?"
#question = "Quantos cursos diurnos tem no campus de patos?"
#question = "Quantos cursos integral tem no campus de patos?"
#question = "Quantos cursos noturnos tem no campus de patos?"
#question = "Quantos cursos noturnos tem na ufcg e que foram criados depois de 2007?"
#question = "Quais são os curriculos atuais, turnos e código do inep de cada curso do campus de pombal?"
question = "Quais são os cinco estudantes com maior cra do curso de ciência da computação do campus campina grande?"

agent.run(question=question)