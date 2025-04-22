from .prompts.prompts import *
from langchain_ollama import ChatOllama
from .agent.agent_disciplinas import AgenteDisciplinas
from .tools.disciplina.get_disciplina import get_disciplina
from .tools.disciplina.get_plano_aulas import get_plano_aulas
from .tools.disciplina.get_todas_disciplinas import get_todas_disciplinas
from .tools.disciplina.get_turmas_disciplina import get_turmas_disciplina
from .tools.disciplina.get_horarios_disciplinas import get_horarios_disciplinas
from .tools.disciplina.get_informacoes_aluno_disciplina import get_informacoes_aluno_disciplina
from .tools.disciplina.get_plano_curso_disciplina import get_plano_de_curso_disciplina
from .tools.disciplina.get_pre_requisitos_disciplina import get_pre_requisitos_disciplina
from .tools.disciplina.get_todas_disciplinas_curso import get_todas_disciplinas_curso
from .tools.disciplina.get_todas_disciplinas_curso import get_disciplinas_curso_por_codigo

tools = [
    get_disciplina, 
    get_horarios_disciplinas,
    get_informacoes_aluno_disciplina,
    get_plano_aulas, 
    get_plano_de_curso_disciplina, 
    get_pre_requisitos_disciplina,
    get_todas_disciplinas_curso,
    get_todas_disciplinas,
    get_turmas_disciplina,
    get_disciplinas_curso_por_codigo
]

agent = AgenteDisciplinas(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)

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
question = "Quais foram os estudantes que passaram na disciplina de Teoria da computação do curso de ciencia da computacao em 2023.2"
agent.run(question=question)