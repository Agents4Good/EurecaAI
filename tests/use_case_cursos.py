from .prompts.prompts import *
from .agent.agent_cursos import AgenteCursos
from langchain_ollama import ChatOllama
from .tools.curso.get_informacoes_cursos import get_informacoes_cursos
from .tools.curso.get_informacoes_estudantes import get_informacoes_estudantes
from .tools.curso.get_todos_curriculos_curso import get_todos_curriculos_curso
from .tools.curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso

tools = [
    get_informacoes_cursos,
    get_informacoes_estudantes,
    get_curriculo_mais_recente_curso,
    get_todos_curriculos_curso
]

#agent = AgentTools(LLM=ChatOpenAI, model="gpt-4o", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)
agent = AgenteCursos(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT1)

question = "quais são os cursos que tiveram o currículo renovado a partir de 2010?"
#question = "Me fale quais foram os cursos que foram criados desde 2010"
#question = "Quais são os cursos de gaduacao do campus de sume?"
#question = "Quantos cursos diurnos tem no campus de patos?"
#question = "Quantos cursos de turno integral tem no campus de patos?"
#question = "Quantos cursos noturnos tem no campus de patos?"

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
#question = "Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?"
#question = "Quantos cursos integral tem no campus de patos?"
#question = "Quais os cursos de graduação noturnos do campus I?"
#question = "Traga todos os cursos do setor de computação"
#question = "Quais são os códigos dos cursos e os nomes dos cursos de licenciatura do campus 1?"
#question = "Qual é o grau do curso de Matemática?"
#question = "Em que campus é oferecido o curso de História?"
#question = "Qual é o turno do curso de Geografia?"
#question = "O curso de Química é oferecido em qual modalidade acadêmica?"
#question = "O curso de Ciências Sociais está disponível em qual campus?"
#question = "Quais são os turnos disponíveis para os cursos de Enfermagem, Farmácia e Nutrição na UFCG?"
#question = "Qual a duração dos cursos de Física e Matemática no campus de Cuité?"
#question = "O curso de Ciências Biológicas, Química e Física são oferecidos em período noturno?"
#question = "Qual é o estudante que tem o maior CRA do curso de ciencia da computacao do campus de campina grande"
question = "Quando o curso de ciencia da computação foi criado?"

agent.run(question=question)