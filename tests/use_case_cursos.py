from .prompts.prompts import *
from .agent.agent_cursos import AgenteCursos
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from .tools.curso.obter_dados_de_curso_especifico import obter_dados_de_curso_especifico
from .tools.curso.obter_dados_de_todos_os_cursos import obter_dados_de_todos_os_cursos
from dotenv import load_dotenv

load_dotenv()

tools = [
    obter_dados_de_curso_especifico,
    obter_dados_de_todos_os_cursos,
]

#agent = AgentTools(LLM=ChatOpenAI, model="gpt-4o", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)
agent = AgenteCursos(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)
#agent = AgenteCursos(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)

question = "quais são os cursos que tiveram o currículo renovado a partir de 2010?"
question = "De todos os cursos de graduação do campus de sume quais deles são relacionados a área de idiomas?" # retornando sem output estrurado correto (VALIDAR!!!)
question = "Quantos cursos diurnos tem no campus de patos?"
#question = "Quantos cursos de turno integral tem no campus de patos?"
#question = "Quantos cursos noturnos tem no campus de patos?"

question = "O curso de Engenharia Elétrica é oferecido em qual campus?"

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
#question = "Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?"

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
#question = "Qual é o estudante que tem o maior CRA do curso de ciencia da computacao do campus de campina grande"
#question = "Quando o curso de ciencia da computação foi criado?"
#question = "Quais os currículos do curso de ciência da computação do campus de campina grande?"

#question = "Quais cursos foram criado em 2009"
#question = "Quando foi criado ciência da computação, quero saber o dia e o mês"
#question = "frances ingles sao ofericidos em que turno?"
question = "computação código?"
agent.run(question=question)