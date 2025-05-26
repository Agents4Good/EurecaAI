from .prompts.prompts import *
from .agent.agent_setores import AgenteSetores
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from .tools.setor.get_estagios import get_estagios
from .tools.setor.get_todos_setores import get_todos_setores
from .tools.setor.get_professores_setor import get_professores_setor

from dotenv import load_dotenv

load_dotenv()

tools = [
    get_estagios,
    get_professores_setor,
    get_todos_setores
]

agent = AgenteSetores(LLM= ChatOllama, model="qwen3:8b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_SETORES_SQL1)
#agent = AgenteSetores(LLM=ChatDeepInfra, model="Qwen/Qwen3-14B", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_SETORES_SQL)

question = "Quais são os professores de ciencia da computacao do campus de campina grande?"# DEVIDO TER PASADO O CURSO ELE PEGOU UNID. ACAD. DE SISTEMAS E COMPUTAÇÃO POR CONTA DO RAG!

#question = "Quais os códigos de todos os setores?" #RESPOSTA MUITO GRANDE, TEM QUE ESPECFICAR O CAMPOUS
#question = "Traga os professores dos estágios do setor UNID. ACAD. DE CIÊNCIAS MÉDICAS do campus de campina grande no ano de 2024" #NOT OK
#question = "Traga o nome dos professores que foram orientadores de estágio do centro de engenharia elétrica e informática no ano de 2024 do campus Campina Grande" #CHAMOU A TOOL CERTA DE PRIMEIRA, MAS CHAMOU OUTRA TOOL EM SEGUIDA
#question = "Traga informações sobre o valor da bolsa dos estágios do campus Campina Grande no ano 2024." #OK
#question = "Quantos estagiarios tiveram no curso de engenharia civil do campus de campina grande em 2024?" #OK
#question = "Qual é o valor médio das bolsas dos estagiarios do curso de engenharia eletrica do campus de campina grande em 2024?" #OK
#question = "Some as bolsas de todos os estagiarios do campus de campina grande em 2024?" #OK
#question = "Some as bolsas de todos os estagiarios da UFCG em 2020?" # PERGUNTA MUITO DEMORADA DEVIDO AOS DADOS

question = "Some as bolsas de todos os estagiarios da UFCG no ano 2020 do campus Campina Grande do curso de engenharia civil?" #OK
question = "Quantos estagiários tem no campus sume em 2024"

agent.run(question=question)