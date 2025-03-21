from prompts.prompts import *
from langchain_ollama import ChatOllama
from agent.agent_tools import AgentTolls
from tools.disciplina.get_disciplina import get_disciplina
from tools.disciplina.get_plano_aulas import get_plano_aulas
from tools.disciplina.get_todas_disciplinas import get_todas_disciplinas
from tools.disciplina.get_turmas_disciplina import get_turmas_disciplina
from tools.disciplina.get_horarios_disciplinas import get_horarios_disciplinas
from tools.disciplina.get_notas_turma_disciplina import get_notas_turma_disciplina
from tools.disciplina.get_plano_curso_disciplina import get_plano_de_curso_disciplina
from tools.disciplina.get_pre_requisitos_disciplina import get_pre_requisitos_disciplina

tools = [
    get_disciplina, 
    get_plano_aulas, 
    get_plano_de_curso_disciplina, 
    get_turmas_disciplina, 
    get_pre_requisitos_disciplina,
    get_horarios_disciplinas,
    get_notas_turma_disciplina,
    get_todas_disciplinas,
]

agent = AgentTolls(LLM=ChatOllama, model="llama3.1", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT2)

question = "Traga informações sobre a disciplina fm cc 2"
agent.run(question=question)