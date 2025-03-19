from .prompts.prompts import *
from .agent.agent_tools import AgentTools
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from .tools.curso.get_curso import get_curso
from .tools.curso.get_cursos import get_cursos
from .tools.curso.get_estudantes_curso import get_estudantes_curso

tools = [
    get_curso,
    get_cursos,
    get_estudantes_curso,
]

#agent = AgentTools(LLM=ChatOpenAI, model="gpt-4o", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)
agent = AgentTools(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)

#question = "quais cursos da ufcg são de bacharelado curriculo?"
#question = "quais são os cursos que tiveram o currículo renovado a partir de 2010?"
question = "quais são os cursos de letras da ufcg do campus de campina grande?"
agent.run(question=question)