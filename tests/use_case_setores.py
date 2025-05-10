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

agent = AgenteSetores(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_SETORES_SQL)

question = "Quais são os professores de ciencia da computacao do campus de campina grande?"
question = "Quais os códigos de todos os setores?"
question = "Traga os professores dos estágios do setor UNID. ACAD. DE CIÊNCIAS MÉDICAS do campus de campina grande no ano de 2024"
question = "Traga o nome dos professores dos estágios do curso de ciência da computação campus Campina Grande no ano de 2024"
question = "O professor Dalton foi orientador de quais estágios no ano 2024, ele é do curso de ciência da computação do campus Campina Grande."
question = "Traga o nome dos professores que foram orientadores de estágio do centro de engenharia elétrica e informática no ano de 2024 do campus Campina Grande"
question = "Traga informações sobre o valor da bolsa dos estágios do campus Campina Grande no ano 2024."
agent.run(question=question)