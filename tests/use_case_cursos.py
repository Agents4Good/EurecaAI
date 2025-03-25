from .prompts.prompts import *
from .agent.agent_tools import AgentTools
from langchain_ollama import ChatOllama
from .tools.curso.get_curso import get_curso
from .tools.curso.get_cursos import get_cursos
from .tools.curso.get_estudantes_curso import get_estudantes

tools = [
    get_curso,
    get_estudantes,
    get_cursos
]

#agent = AgentTools(LLM=ChatOpenAI, model="gpt-4o", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)
agent = AgentTools(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)

#question = "quais cursos da ufcg são de bacharelado curriculo?"
#question = "quais são os cursos que tiveram o currículo renovado a partir de 2010?"
#question = "Quantos cursos existem no campus de campina grande?"
#question = "Qual é o código do curso de ciencia da computação?"
#question = "Me fale quais foram os cursos que foram criados desde 2010"
#question = "Quais são os cursos de gaduacao do campus de sume?"
#question = "Quantos cursos diurnos tem no campus de patos?"
#question = "Quantos cursos de turno integral tem no campus de patos?"
#question = "Quantos cursos noturnos tem no campus de patos?"
#question = "Quantos cursos noturnos tem na ufcg e que foram criados depois de 2007?"
#question = "Quais são os curriculos atuais, turnos e código do inep de cada curso do campus de pombal?"
#question = "Quais cursos de graduação estão disponíveis no campus de Campina Grande?"
#question = "Qual é o turno do curso de Medicina?"

#question = "Em que ano começou o curso de Arquitetura e Urbanismo?"
#question = "O curso de Engenharia Elétrica é oferecido em qual campus?"

#question = "Quais são os cinco estudantes com maior cra do curso de ciência da computação do campus campina grande?"
#question = "Quantas estudantes mulheres tem no curso de engenharia mecanica do campus de campina grande"
#question = "Quantas estudantes mulheres tem CRA acima de 8,5 no curso de engenharia eletica do campus de campina grande"
#question = "Existe algum deficiente no curso de ciencia da computação do campus de campina grande"
#question = "Quantos estudantes que estudam durante a noite no campus de campina grande?"
#question = "Existem estudantes que estudam durante a noite no campus de pombal?"
#question = "Existem quantos estudantes casados e solteiros no curso de enhenharia de materiais do campus de campina grande?" # Erro
#question = "Existem quantos estudantes de escola pública?"
#question = "Quantos estudantes de escola pública existem no curso de medicina no campus de campina grande?"
#question = "Quantos estudantes de escola pública e particular no curso de medicina do campus de campina grande?"
question = "Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?"
agent.run(question=question)