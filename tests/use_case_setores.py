from prompts.prompts import *
from agent.agent_tools import AgentTolls
from langchain_ollama import ChatOllama
from tools.setor.get_estagios import get_estagios
from tools.setor.utils import get_setor_most_similar
from tools.setor.get_todos_setores import get_todos_setores
from tools.setor.get_professores_setor import get_professores_setor

tools = [
    get_estagios,
    get_professores_setor,
    get_todos_setores,
    get_setor_most_similar
]

agent = AgentTolls(LLM=ChatOllama, model="llama3.2:3b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)

question = "Quais são os professores de ciencia da computacao do campus de campina grande?"
agent.run(question=question)