from .prompts.prompts import *
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from .agent.agent_disciplinas import AgenteDisciplinas
from .tools.disciplina.get_plano_de_aulas import get_plano_de_aulas
from .tools.disciplina.get_turmas_disciplina import get_turmas_disciplina
from .tools.disciplina.get_horarios_disciplina import get_horarios_disciplina
from .tools.disciplina.get_notas_disciplina import get_matriculas_disciplina
from .tools.disciplina.get_plano_de_curso_disciplina import get_plano_de_curso_disciplina
from .tools.disciplina.get_pre_requisitos_disciplina import get_pre_requisitos_disciplina
from .tools.disciplina.get_disciplinas import get_disciplinas

tools = [
    get_horarios_disciplina,
    get_matriculas_disciplina,
    get_plano_de_aulas, 
    #get_plano_de_curso_disciplina, 
    get_pre_requisitos_disciplina,
    get_disciplinas,
    #get_turmas_disciplina
]

#print(get_disciplinas.args_schema.schema())

agent = AgenteDisciplinas(LLM=ChatOllama, model="qwen3", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)
#agent = AgenteDisciplinas(LLM=ChatDeepInfra, model="meta-llama/Llama-3.3-70B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)

# Outros

#question = "Qual é a sala da disiciplina Fundamentos de Matemática para Ciência da Computação 2?" # ToolCall - OK

question = "Quantas disciplinas existem no curso de ciência da computação do campus de campina grande?"
question = "Eu estava curioso para saber quantas disciplinas há no curso de engenharia elétrica"
question = "Quantas disciplinas do curso de engenharia mecanica do campus de campina grande tem 4 creditos?"
question = "Quero o nome e os creditos de todas as disciplina que tenha 60 horas de aula para o curso de engenharia de producao do campus de campina grande"
question = "Quero saber o nome e os creditos em medicina de campina grande"
question = "Quantas disciplinas tem no curriculo de 2017 no curso de ciencia da computação do campus de campina grande"
question = "Quais disciplinas do curso de Ciência da Computação do campus de Campina Grande têm mais de 4 créditos?"
question = "Me mostre as disciplinas com carga horária teórica semanal maior que 2 do curso de Ciência da Computação de Campina Grande."
question = "Quais são as disciplinas complementares do curso de Ciência da Computação do campus de Campina Grande?"
question = "Liste o nome das disciplinas do curso de Ciência da Computação em Campina Grande com carga horária prática semanal igual a 0."
# question = "Quais as notas dos estudantes da disciplina de inteligencia artificial do curso de ciencia da computacao no periodo 2023.1?" # ToolCall - OK
# question = "Quais disciplinas da Ciência da Computação em Campina Grande pertencem ao setor de Engenharia Elétrica?"
# question = "Quais disciplinas do currículo 2017 do curso de Ciência da Computação em Campina Grande têm mais de um crédito, carga prática semanal diferente de zero, e são do tipo Normal?"
# question = "Liste todas as disciplinas do curso de Ciência da Computação do campus de Campina Grande com carga horária teórica maior que 2 e carga horária prática menor ou igual a 2, independentemente do currículo."
# question = "Quais são os nomes dos setores com mais de 5 disciplinas associadas no curso de Ciência da Computação do campus de Campina Grande"
# question = "Quais disciplinas do currículo 2023 da Ciência da Computação em Campina Grande têm mais carga horária teórica do que prática?"
# question = "Liste as disciplinas que têm carga horária total superior à média do curso de Ciência da Computação no campus de Campina Grande, independentemente do currículo."





# Notas permutação
# Campo: matricula_do_estudante
question = "Quais são as matrículas dos estudantes que cursaram Teoria da Computação no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Liste as matrículas dos alunos que fizeram a disciplina de Teoria da Computação no campus de Campina Grande."
#question = "Me mostre quem, por matrícula, cursou Teoria da Computação na Ciência da Computação de Campina Grande."

# Campo: periodo
#question = "Em quais períodos os alunos da Ciência da Computação do campus de Campina Grande cursaram Teoria da Computação?"
#question = "Qual foi o período em que os estudantes fizeram Teoria da Computação na Ciência da Computação em Campina Grande?"
#question = "Liste os diferentes períodos em que a disciplina de Teoria da Computação foi ofertada no curso de Ciência da Computação do campus de Campina Grande."

# Campo: turma
#question = "Quais turmas de Teoria da Computação existem no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Me informe as turmas da disciplina Teoria da Computação ofertadas na Ciência da Computação de Campina Grande."
#question = "Liste os códigos de turma de Teoria da Computação do campus de Campina Grande para o curso de Ciência da Computação."

# Campo: status
#question = "Quantos alunos foram aprovados em Teoria da Computação no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Quais estudantes foram reprovados em Teoria da Computação na Ciência da Computação de Campina Grande?"
#question = "Quem trancou a disciplina Teoria da Computação no curso de Ciência da Computação de Campina Grande?"
#question = "Liste os estudantes com status de 'Reprovado por Falta' ou 'Reprovado por Nota' na disciplina Teoria da Computação do curso de Ciência da Computação do campus de Campina Grande."
#question = "Me mostre os estudantes que foram aprovados ou reprovados por falta em Teoria da Computação no campus de Campina Grande."

# Campo: media_final
#question = "Quais foram as médias finais dos estudantes em Teoria da Computação no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Liste os alunos com média final maior que 7 na disciplina Teoria da Computação da Ciência da Computação em Campina Grande."
#question = "Quais estudantes tiraram média menor que 5 em Teoria da Computação na Ciência da Computação do campus de Campina Grande?"
#question = "Qual foi a maior média final na disciplina de Teoria da Computação no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Me diga quais alunos tiraram exatamente 10 em Teoria da Computação em Campina Grande, no curso de Ciência da Computação."

# Campo: dispensas
#question = "Quais alunos dispensaram a disciplina Teoria da Computação no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Me mostre quem não dispensou Teoria da Computação na Ciência da Computação de Campina Grande."
#question = "Quantos estudantes conseguiram dispensa na disciplina Teoria da Computação, no curso de Ciência da Computação do campus de Campina Grande?"
#question = "Liste os alunos que cursaram Teoria da Computação e não tiveram dispensa, no curso de Ciência da Computação em Campina Grande."


agent.run(question=question)
