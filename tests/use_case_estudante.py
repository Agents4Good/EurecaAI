from .prompts.prompts import *
from langchain_ollama import ChatOllama
from .agent.agent_estudante import AgenteEstudante
from .tools.estudante.obter_dados_gerais_de_todos_estudantes import obter_dados_gerais_de_todos_estudantes
from langchain_community.chat_models import ChatDeepInfra
from dotenv import load_dotenv


load_dotenv()

tools = [
    obter_dados_gerais_de_todos_estudantes
]   

agent = AgenteEstudante(LLM=ChatOllama, model="qwen3:8b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_ESTUDANTE_SQL)
#agent = AgenteEstudante(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_ESTUDANTE_SQL)
#question = "Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?"

question = "Qual é o CRA de Matheus Hensley?"
question = "Quantos estrangeiros tem no curso?"
question = "Quantos estudantes tem CRA acima da média?"
question = "Quantos estudantes vieram do estado da paraiba?"
question = "De onde vem os estudantes do curso por estado? Me mostre pra cada estado do país"
question = "Quais são os 5 estudantes com maior cra do curso de ciência da computação do campus de campina grande?"
question = "Quantos estudantes que estudam a noite no campus de campina grande?"
question = "Existem quantos estudantes casados e solteiros no curso de engenharia de materiais do campus de campina grande?"
question = "Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?"
question = "Quem são os estudantes que estão no 5 período do curso?"
question = "Quem sao os estudantes que transferiram de curso que são da cidade de caturite?"
question = "Quem são os alunos de escola pública que estudam no curso de ciencia da computacao que vieram da cidade de aroeiras"
question = "qual é o índice de eficiência acadêmica de caique?"
question = "quantos estudantes sao pardos ou pretos no curso de ciencia da computacao do campus de campina grande?"

#question = "quantas pessoas tem renda entre 1 a 10 salario minimo do campus Campina Grande?"  #VERIFICAR DEPOIS
#TALVEZ SEJA NECESSSARIO INFORMAR O CAMPUS E O NOME DO CURSO?


#question = "Quais são os cinco estudantes com maior cra do curso de ciência da computação do campus campina grande?"
#question = "Quantas estudantes mulheres tem no curso de engenharia mecanica do campus de campina grande"
#question = "Quantas estudantes mulheres tem CRA acima de 8,5 no curso de engenharia eletica do campus de campina grande"
#question = "Existe algum deficiente no curso de ciencia da computação do campus de campina grande"
#question = "Quantos estudantes que estudam durante a noite no campus de campina grande?"
#question = "Existem estudantes que estudam durante a noite no campus de pombal?"
#question = "Existem quantos estudantes casados e solteiros no curso de enhenharia de materiais do campus de campina grande?" #V
#question = "Existem quantos estudantes de escola pública?"
#question = "Quantos estudantes de escola pública existem no curso de medicina no campus de campina grande?"
#question = "Quantos estudantes de escola pública e particular no curso de medicina do campus de campina grande?"
#question = "Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?"
#question = "Quantos estudantes solteiros existem no curso de ciência da computação do campus Campina Grande?"


#question = "Quantas estudantes mulheres existem no curso de ciência da computação do campus Campina Grande"
#question = "Qual é a proporção de meninas com relação aos meninos no curso de ciência da cumptação cmapus campina grande"
#question = "Qual a quantidade de estudantes do sexo feminino no curso de ciência da computação do campus Campina Grande?"
#question = "QUero saber quantas meninas existem no curso de ciência da computação campus campina grande"
question = "De onde vem os estudantes do curso de ciência da computação do campus Campina grande por estado? Me mostre pra cada estado do país"
#question = "Traga o nome dos estudantes do curso de ciência da computação do campus Campina Grande que tema deficiência B10"
#question = "Quantos estudantes internacionais existem no curso de ciência da computação do campus Campina Grande?"
agent.run(question=question)
