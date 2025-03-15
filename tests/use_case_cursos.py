from .prompts.prompts import *
from .agent.agent_tools import AgentTools
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
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

question = "Qual o nome do setor e o seu código para letras inglês e francês?"
#question = "quais são os cursos de letras da ufcg do campus de campina grande?"
#question = "quero saber a carga horária e os créditos do curso de ciência da computação"
agent.run(question=question)