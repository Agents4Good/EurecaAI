from .prompts.prompts import *
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from .agent.agent_disciplinas import AgenteDisciplinas
from .tools.disciplina.get_plano_de_aulas import get_plano_de_aulas
from .tools.disciplina.get_turmas_disciplina import get_turmas_disciplina
from .tools.disciplina.get_horarios_disciplina import get_horarios_disciplina
from .tools.disciplina.get_notas_disciplina import get_notas_disciplina
from .tools.disciplina.get_plano_de_curso_disciplina import get_plano_de_curso_disciplina
from .tools.disciplina.get_pre_requisitos_disciplina import get_pre_requisitos_disciplina
from .tools.disciplina.get_disciplinas import get_disciplinas

tools = [
    get_horarios_disciplina,
    get_notas_disciplina,
    get_plano_de_aulas, 
    get_plano_de_curso_disciplina, 
    get_pre_requisitos_disciplina,
    get_disciplinas,
    get_turmas_disciplina
]

#print(get_disciplinas.args_schema.schema())

agent = AgenteDisciplinas(LLM=ChatOllama, model="qwen3:4b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)
#agent = AgenteDisciplinas(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)

#question = "Quais foram a média das notas na turma 1 da disciplina de inteligencia artificial do curso de cincia da computação no periodo 2023.2?"
#question = "Qual são os assuntos de EDA do curso ciência da computação?"
#question = "Qual o código da disciplina fmcc2 do curso ciência da computação?"
#question = "Quantos alunos passaram na disciplinas de fmcc 2 no período 2023.2 do curso de ciencia da computacao?"
#question = "Quantas pessoas trancaram a disciplina de oac do periodo 2023.2 do curso de ciencia da computacao?"
#question = "Quantas pessoas reprovaram por nota na disciplina de tc do periodo 2023.2 do curso de ciencia da computacao?"
#question = "Quantas pessoas reprovaram por falta a disciplina de tc do periodo 2023.2 do curso de ciencia da computacao?"
#question = "Quantas pessoas reprovaram a disciplina de tc do periodo 2023.2 do curso de ciencia da computacao?"
#question = "Me diga 5 nomes e suas notas dos alunos que tiraram a maior nota na turma 1 da disciplina de teoria da computacao do curso de ciencia da computacao no periodo 2023.2"
#question = "Qual foi a menor nota dos alunos na disciplina de teoria da computação do curso de ciência da computação em 2023.2?"
#question = "Quais foram os estudantes que passaram na disciplina de Teoria da computação do curso de ciencia da computacao em 2023.2"
question = "Quais foram os estudantes que passaram na disciplina de Teoria da computação do curso de ciencia da computacao em 2023.2 no campus Campina Grande?"
#question = "Quero o nome do estudante que tem a maior nota na turma 1 na disciplina de Teoria da computação do curso de ciencia da computação do campus de campina grande no período 2023.2?"
#question = "Quantas disciplinas tem no curso de ciência da computação no curriculo 2023"
question = "Qual é o horária da disciplina de redes de computadores do curso de ciencia da computacao do campus de campina grande?"
question = "Quais são as tumas de teoria da computação do curso de ciencia da computacao?"
question = "Quais disciplina preciso para cursar a disciplina de teoria da computacao do curso de ciencia da computacao do campus de campina grande?"
#question = "Quantas disciplinas tem no curso de ciência da computação no curriculo 2023"
agent.run(question=question)