from prompts.prompts import *
from agent.agent_tools import AgentTolls
from langchain_ollama import ChatOllama
from tools.curso.get_curso import get_curso
from tools.curso.get_cursos import get_cursos
from tools.curso.utils import get_curso_most_similar
from tools.curso.get_estudantes_curso import get_estudantes_curso
from tools.curso.get_todos_curriculos_curso import get_todos_curriculos_curso
from tools.curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso

tools = [
    get_curso,
    get_cursos, 
    get_estudantes_curso,
    get_curso_most_similar,
    get_todos_curriculos_curso,
    get_curriculo_mais_recente_curso,
]

agent = AgentTolls(LLM=ChatOllama, model="llama3.2:3b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)

question = "Quais são os cursos da UFCG?"
agent.run(question=question)