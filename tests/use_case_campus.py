from .prompts.prompts import *
from langchain_ollama import ChatOllama
from .agent.agent_campus import AgenteCampus
from .tools.campus.get_campi import get_campi
from .tools.campus.get_calendarios import get_calendarios
from .tools.campus.get_periodo_mais_recente import get_periodo_mais_recente

tools = [
    get_campi,
    get_calendarios, 
    get_periodo_mais_recente
]

agent = AgenteCampus(LLM=ChatOllama, model="qwen3:8b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_CAMPUS_SQL)

question = "Quais são os campus da UFCG?"
question = "Quando começa o período 2024.2"
agent.run(question=question)