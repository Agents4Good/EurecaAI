from prompts.prompts import *
from langchain_ollama import ChatOllama
from agent.agent_tools import AgentTolls
from tools.campus.get_campi import get_campi
from tools.campus.get_calendarios import get_calendarios
from tools.campus.get_periodo_mais_recente import get_periodo_mais_recente

tools = [
    get_campi,
    get_calendarios, 
    get_periodo_mais_recente
]

agent = AgentTolls(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)

question = "Quais são os campus da UFCG?"
agent.run(question=question)