from .prompts.prompts import *
from .agent.agent_setores import AgenteSetores
from langchain_ollama import ChatOllama
from .tools.setor.get_estagios import get_estagios
from .tools.setor.get_todos_setores import get_todos_setores
from .tools.setor.get_professores_setor import get_professores_setor

tools = [
    get_estagios,
    get_professores_setor,
    get_todos_setores
]

agent = AgenteSetores(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_SETORES_SQL)

question = "Quais são os professores de ciencia da computacao do campus de campina grande?"
agent.run(question=question)