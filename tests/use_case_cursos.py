from .prompts.prompts import *
from .agent.agent_cursos import AgenteCursos
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra

from .tools.curso.obter_dados_de_curso_especifico import obter_dados_de_curso_especifico
from .tools.curso.obter_dados_de_todos_os_cursos import obter_dados_de_todos_os_cursos
from .tools.curso.obter_grade_curricular_curso import obter_grade_curricular_curso

from dotenv import load_dotenv

load_dotenv()

tools = [
    obter_dados_de_curso_especifico,
    obter_dados_de_todos_os_cursos
]

#agent = AgenteCursos(LLM=ChatOllama, model="qwen3:4b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)
#agent = AgenteCursos(LLM=ChatDeepInfra, model="meta-llama/Llama-3.3-70B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)
agent = AgenteCursos(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)

question = "quais são os cursos que tiveram o currículo renovado a partir de 2010?"
question = "De todos os cursos de graduação do campus de sume quais deles são relacionados a área de idiomas?" # retornando sem output estrurado correto (VALIDAR!!!)
question = "Quantos cursos diurnos tem no campus de patos?"
#question = "Quantos cursos de turno integral tem no campus de patos?"
#question = "Quantos cursos noturnos tem no campus de patos?"

question = "O curso de Engenharia Elétrica é oferecido em qual campus?"

#question = "Quais os cursos de graduação noturnos do campus I?"
#question = "Traga todos os cursos do setor de computação"
question = "Quais são os códigos dos cursos e os nomes dos cursos de licenciatura do campus da ufcg?"
#question = "Qual é o grau do curso de Matemática?"
#question = "Em que campus é oferecido o curso de História?"
#question = "Qual é o turno do curso de Geografia?"
#question = "O curso de Química é oferecido em qual modalidade acadêmica?"
#question = "O curso de Ciências Sociais está disponível em qual campus?"
#question = "Quais são os turnos disponíveis para os cursos de Enfermagem, Farmácia e Nutrição na UFCG?"
#question = "Qual a duração dos cursos de Física e Matemática no campus de Cuité?"
#question = "O curso de Ciências Biológicas, Química e Física são oferecidos em período noturno?"
#question = "Quando o curso de ciencia da computação foi criado?"
#question = "Quais os currículos do curso de ciência da computação do campus de campina grande?"

#question = "Quais cursos foram criado em 2009"
#question = "Quando foi criado ciência da computação, quero saber o dia e o mês"
#question = "frances ingles sao ofericidos em que turno?"
#question = "computação código?"
#question = "qual o curso que mexe com compiuter?"
agent.run(question=question)