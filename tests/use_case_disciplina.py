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

print(get_disciplinas.args_schema.schema())

#agent = AgenteDisciplinas(LLM=ChatOllama, model="qwen3:4b", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)
agent = AgenteDisciplinas(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", tools=tools, temperatura=0, prompt=ZERO_SHOT_PROMPT_DISCIPLINAS_SQL)
question = "Quais foram a média das notas na turma 1 da disciplina de inteligencia artificial do curso de cincia da computação no periodo 2023.2?" # ToolCall - OK
question = "Qual são os assuntos de EDA do curso ciência da computação?" # ToolCall - OK
question = "Qual o código da disciplina fmcc2 do curso ciência da computação?" # ToolCall - OK
question = "Quantos alunos passaram na disciplinas de fmcc 2 no período 2023.2 do curso de ciencia da computacao?" # ToolCall - OK
question = "Quantas pessoas trancaram a disciplina de oac do periodo 2023.2 do curso de ciencia da computacao?" # ToolCall - OK
question = "Quantas pessoas reprovaram por nota na disciplina de tc do periodo 2023.2 do curso de ciencia da computacao?" # ToolCall - OK
question = "Quantas pessoas reprovaram por falta a disciplina de tc do periodo 2023.2 do curso de ciencia da computacao?" # ToolCall - OK
question = "Quantas pessoas reprovaram a disciplina de tc do periodo 2023.2 do curso de ciencia da computacao?" # ToolCall - OK
question = "Me diga 5 nomes e suas notas dos alunos que tiraram a maior nota na turma 1 da disciplina de teoria da computacao do curso de ciencia da computacao no periodo 2023.2" # ToolCall - OK
question = "Qual foi a menor nota dos alunos na disciplina de teoria da computação do curso de ciência da computação em 2023.2?"  # ToolCall - OK
question = "Quais foram os estudantes que passaram na disciplina de Teoria da computação do curso de ciencia da computacao em 2023.2"  # ToolCall - OK
question = "Quero o nome do estudante que tem a maior nota na turma 1 na disciplina de Teoria da computação do curso de ciencia da computação do campus de campina grande no período 2023.2?"  # ToolCall - OK
question = "Quantas disciplinas tem no curso de ciência da computação no curriculo 2023" # ToolCall - OK
question = "Qual é o horária da disciplina de redes de computadores do curso de ciencia da computacao do campus de campina grande?" # ToolCall - OK
question = "Quais são as turmas de teoria da computação do curso de ciencia da computacao?" # ToolCall - OK
question = "Quais disciplina preciso para cursar a disciplina de teoria da computacao do curso de ciencia da computacao do campus de campina grande?" # ToolCall - OK

# Disciplinas

question = "Qual é a carga horária teórica semanal da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "A disciplina Álgebra Linear I tem carga horária prática no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Quantos créditos a disciplina Álgebra Linear I possui no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Qual o total de horas da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Qual o setor responsável pela disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Qual o setor da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK

question = "Quais disciplinas fazem parte do curso de Ciência da Computação no campus de Campina Grande, no currículo de 2023?"# ToolCall-OK
question = "Quantas disciplinas existem no curso de Ciência da Computação no campus de Campina Grande, no currículo de 2023?" # ToolCall-OK
question = "Quais são os nomes das disciplinas ofertadas no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande têm carga horária prática semanal diferente de zero?" # ToolCall-OK
question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande são do tipo 'Normal'?" # ToolCall errou, passou codigo_disciplina: Tipo: Normal

question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande possuem 4 créditos?" # ToolCall-OK
question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande têm carga horária total maior que 60 horas?" # ToolCall-OK
question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande possuem somente carga teórica e nenhuma carga prática?" # ToolCall-OK
question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande têm carga prática semanal?" # ToolCall-OK
question = "Qual é a média de créditos das disciplinas do curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK

question = "Quais disciplinas do curso de Ciência da Computação no campus de Campina Grande são ofertadas pelo setor UNID. ACAD. DE MATEMÁTICA?" # ToolCall-OK
question = "Existem disciplinas do curso de Ciência da Computação no campus de Campina Grande ofertadas por mais de um setor?" # ToolCall-OK
question = "Quantas disciplinas do curso de Ciência da Computação no campus de Campina Grande são ofertadas por setores da área de exatas?" # ToolCall-OK
question = "Qual é o campus onde a disciplina Álgebra Linear I é ofertada no curso de Ciência da Computação?" # ToolCall-OK
question = "Há outras disciplinas além de Álgebra Linear I ofertadas pelo setor UNID. ACAD. DE MATEMÁTICA no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall errou, codigo_disciplina: Álgebra Linear I 

question = "Quais disciplinas fazem parte do curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK
question = "Quantas disciplinas existem no curso de Engenharia Elétrica no campus de Cajazeiras no currículo de 2022?" # ToolCall-OK
question = "Quais disciplinas do curso de Engenharia Elétrica no campus de Cajazeiras possuem carga horária prática semanal?" # ToolCall-OK
question = "Qual a disciplina com maior número de créditos no curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK
question = "Quais disciplinas do curso de Engenharia Elétrica no campus de Cajazeiras são ofertadas pelo setor de Física?" # ToolCall-OK

question = "Quais disciplinas fazem parte do curso de Administração no campus de Patos?" # ToolCall-OK
question = "Quais disciplinas do curso de Administração no campus de Patos possuem apenas carga horária teórica?" # ToolCall-OK
question = "Quantos créditos têm as disciplinas do curso de Administração no campus de Patos em média?" # ToolCall-OK
question = "Quais disciplinas do curso de Administração no campus de Patos são ofertadas pelo setor de Ciências Sociais Aplicadas?" # ToolCall-OK
question = "Qual a carga horária total da disciplina Fundamentos de Administração no curso de Administração no campus de Patos?" #ToolCall errou, codigo_disciplina: Fundamentos de Administração

question = "Quais disciplinas fazem parte do curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK
question = "Quais disciplinas do curso de Sistemas de Informação no campus de Sousa possuem carga prática semanal?" # ToolCall-OK
question = "Quais disciplinas do curso de Sistemas de Informação no campus de Sousa são ofertadas pelo setor de Computação?" # ToolCall-OK
question = "Qual a disciplina com menor carga horária total no curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK
question = "Quais disciplinas do curso de Sistemas de Informação no campus de Sousa têm 3 créditos?" # ToolCall errou, codigo_disciplina: 3


# Notas na disciplina

question = "Quais foram as médias finais dos alunos na disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Quantos alunos foram aprovados na disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Quantos alunos foram reprovados por nota na disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Algum aluno foi dispensado da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Qual é a média geral da turma na disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK

question = "Quantos alunos foram aprovados na disciplina Cálculo Diferencial I do curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK
question = "Qual a média final de cada estudante na disciplina Cálculo Diferencial I do curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK
question = "Há estudantes com status de 'reprovado' na disciplina Cálculo Diferencial I do curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK
question = "Quais estudantes foram dispensados da disciplina Cálculo Diferencial I no curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK
question = "Qual estudante obteve a maior média final na disciplina Cálculo Diferencial I do curso de Engenharia Elétrica no campus de Cajazeiras?" # ToolCall-OK

question = "Quais alunos foram aprovados na disciplina Bioquímica I do curso de Engenharia de Alimentos no campus de Pombal?" # ToolCall-OK
question = "Algum aluno foi dispensado da disciplina Bioquímica I no curso de Engenharia de Alimentos no campus de Pombal?" # ToolCall-OK
question = "Qual a média final da turma na disciplina Bioquímica I do curso de Engenharia de Alimentos no campus de Pombal?" # ToolCall-OK
question = "Qual o status de cada estudante na disciplina Bioquímica I do curso de Engenharia de Alimentos no campus de Pombal?" # ToolCall-OK
question = "Quantos alunos foram reprovados na disciplina Bioquímica I do curso de Engenharia de Alimentos no campus de Pombal?" # ToolCall-OK

question = "Quais foram os estudantes aprovados na disciplina Fundamentos de Economia no curso de Administração no campus de Patos?" # ToolCall-OK
question = "Qual foi a média final dos alunos na disciplina Fundamentos de Economia no curso de Administração no campus de Patos?" # ToolCall-OK
question = "Quantos estudantes foram reprovados por nota na disciplina Fundamentos de Economia no curso de Administração no campus de Patos?" # ToolCall-OK
question = "Existe algum aluno dispensado da disciplina Fundamentos de Economia no curso de Administração no campus de Patos?" # ToolCall-OK
question = "Quais são as matrículas dos alunos com maior média na disciplina Fundamentos de Economia no curso de Administração no campus de Patos?" # ToolCall errou, periodo: 1. 

question = "Quem foi aprovado na disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK
question = "Quantos estudantes foram dispensados da disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK
question = "Qual foi a média final da turma na disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK
question = "Quais alunos tiveram status de 'reprovado' na disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK
question = "Quais alunos obtiveram média final superior a 8 na disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Sousa?" # ToolCall-OK

question = "Quais foram as médias finais dos alunos na disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande na turma 1?" # ToolCall-OK
question = "Quantos alunos foram aprovados na disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande na turma 3 do periodo 2023.2?" # ToolCall-OK
question = "Quantos alunos foram reprovados por nota na disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande em todas as turma?" # ToolCall-OK
question = "Algum aluno foi dispensado da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande no periodo 2024.1?" # ToolCall-OK
question = "Qual é a média geral da turma na disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande nos perioso 2023.2 e 2024.1 na turma 1 e 2?" # ToolCall errou, turma: 1,2; periodo: 2023.2,2024.1

# Horários

question = "Qual o dia e horário da disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Em qual sala acontece a disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Qual o setor responsável pela disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK

question = "Qual o turno da disciplina Cálculo Diferencial do curso de Engenharia Civil no campus de Patos?" # ToolCall-OK
question = "Em que dia da semana acontece a disciplina Cálculo Diferencial no curso de Engenharia Civil no campus de Patos?" # ToolCall-OK
question = "Quantas horas tem a disciplina Cálculo Diferencial do curso de Engenharia Civil no campus de Patos?" # ToolCall-OK
question = "Qual a sala da disciplina Cálculo Diferencial do curso de Engenharia Civil no campus de Patos?" # ToolCall-OK

question = "Qual o dia e horário da disciplina Estrutura de Dados do curso de Sistemas de Informação no campus de Cajazeiras?" # ToolCall-OK
question = "Qual o setor responsável pela disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Cajazeiras?" # ToolCall-OK
question = "Qual o código da sala da disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Cajazeiras na turma 1?" # ToolCall-OK
question = "Qual o código da sala da disciplina Estrutura de Dados no curso de Sistemas de Informação no campus de Cajazeiras turma 2, curriculo 2010 e periodo 2024.2?" # ToolCall-OK

question = "Quando ocorre a disciplina Biologia Celular do curso de Ciências Biológicas no campus de Cuité turma 2?" # ToolCall-OK
question = "Quando ocorreu a disciplina Biologia Celular do curso de Ciências Biológicas no campus de Cuité turma 2 no periodo 2023.2?" # ToolCall-OK
question = "Qual o horário da disciplina Biologia Celular do curso de Ciências Biológicas no campus de Cuité no curriculo 2010 periodo 2024.1?" # ToolCall-OK
question = "Quantos créditos tem a disciplina Biologia Celular do curso de Ciências Biológicas no campus de Cuité?" # ToolCall-OK


# Aula

question = "Qual o conteúdo abordado na aula 5 da disciplina Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande?" # ToolCall-OK
question = "Quantas horas teve a primeira aula de Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # Confundiu com get_horarios_disciplina
question = "Em que data aconteceu a aula 5 da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # Confundiu com get_horarios_disciplina
question = "Quais tópicos foram discutidos em Álgebra Linear I do curso de Ciência da Computação no campus de Campina Grande no dia 21/02/2020?" # ToolCall-OK
question = "Quantas aulas já foram ministradas da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande no período 2020.1?" # Confundiu com get_horarios_disciplina

question = "Quais foram os assuntos abordados nas aulas de Cálculo Diferencial e Integral I no curso de Engenharia Civil no campus de Cajazeiras?" # ToolCall - OK
question = "Quantas horas teve a aula 3 de Cálculo Diferencial e Integral I no curso de Engenharia Civil no campus de Cajazeiras?" # 
question = "O que foi ensinado na aula de 05/03/2020 da disciplina Cálculo Diferencial e Integral I no curso de Engenharia Civil no campus de Cajazeiras?" # ToolCall errou, periodo: 1/2020 e curriculo: 1/2020. 
question = "Em qual data aconteceu a aula 2 de Cálculo Diferencial e Integral I no curso de Engenharia Civil no campus de Cajazeiras?" # ToolCall errou, chamou get_horarios_disciplina
question = "Qual o conteúdo na primeira aula de Cálculo Diferencial e Integral I no curso de Engenharia Civil no campus de Cajazeiras?" # ToolCall - OK  

question = "Quais assuntos foram tratados na aula 4 da disciplina Estruturas de Dados no curso de Engenharia de Software no campus de Patos?" # ToolCall - OK
question = "Quando foi realizada a aula 2 de Estruturas de Dados no curso de Engenharia de Software no campus de Patos?" # ToolCall errou, get_horarios_disciplina chamada
question = "Quantas horas teve a aula 1 de Estruturas de Dados no curso de Engenharia de Software no campus de Patos?" # ToolCall errou, get_horarios_disciplina chamada
question = "O que foi ensinado em Estruturas de Dados no curso de Engenharia de Software no campus de Patos no dia 14/03/2020?" # ToolCall - OK
question = "Qual é o cronograma de aulas da disciplina Estruturas de Dados no curso de Engenharia de Software no campus de Patos?" # ToolCall - OK

question = "Qual o conteúdo programático das aulas da disciplina Fundamentos de Programação no curso de Sistemas de Informação no campus de Sousa?" # ToolCall - OK
question = "Quantas aulas já foram dadas da disciplina Fundamentos de Programação no curso de Sistemas de Informação no campus de Sousa?" # ToolCall errou, chamou get_horarios_disciplina
question = "O que foi discutido na aula 3 da disciplina Fundamentos de Programação no curso de Sistemas de Informação no campus de Sousa?" # ToolCall errou, tool certa, mas numero_da_turma: 3
question = "Em que data foi ministrada a aula 5 de Fundamentos de Programação no curso de Sistemas de Informação no campus de Sousa?" # ToolCall errou, tool certa, mas numero_da_turma: 5
question = "Quantas horas teve cada aula da disciplina Fundamentos de Programação no curso de Sistemas de Informação no campus de Sousa?" # ToolCall errou, chamou get_horarios_disciplina


# Plano de Aulas

question = "Qual é a ementa da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall errou, chamou get_disciplinas
question = "Quais são os objetivos da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall - OK
question = "Qual o conteúdo programático da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall - OK
question = "Quais capítulos compõem o plano de curso da disciplina Álgebra Linear I no curso de Ciência da Computação em Campina Grande?" # ToolCall - OK
question = "Qual é o conteúdo da disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" 
# question = "Quais são as referências bibliográficas da disciplina Álgebra Linear I no curso de Ciência da Computação em Campina Grande?" # ToolCall - OK

question = "Como é a metodologia de ensino da disciplina Álgebra Linear I no curso de Ciência da Computação em Campina Grande?" # ToolCall errou, chamou pre_requisitos
question = "Qual o método de avaliação utilizado na disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall champu pre_requisitos
question = "De que forma os trabalhos práticos são utilizados na disciplina Álgebra Linear I em Ciência da Computação no campus de Campina Grande?"
question = "Quais são as referências bibliográficas da disciplina Álgebra Linear I no curso de Ciência da Computação em Campina Grande?" # ToolCall - OK

question = "Quais são as referências bibliográficas da disciplina Álgebra Linear I no curso de Ciência da Computação em Campina Grande?" # ToolCall - OK
question = "Quais livros são recomendados para a disciplina Álgebra Linear I no curso de Ciência da Computação no campus de Campina Grande?" # ToolCall - OK
question = "Quem são os autores recomendados na bibliografia da disciplina Álgebra Linear I no curso de Ciência da Computação em Campina Grande?" # ToolCall - OK

# Pre-requisitos

question = "Quais são os pré-requisitos da disciplina Cálculo III no curso de Engenharia Elétrica em Campina Grande, currículo 2018?" # ToolCall - OK
question = "Preciso ter cursado alguma disciplina antes de me matricular em Eletromagnetismo I na Engenharia Elétrica em Campina Grande?" # ToolCall - OK
question = "Existe algum pré-requisito para cursar Estruturas de Dados na Ciência da Computação no campus de Cajazeiras?" # ToolCall - OK
question = "Quais disciplinas preciso ter feito antes para me matricular em Sistemas Operacionais no curso de Ciência da Computação em Cajazeiras?" # ToolCall - OK
question = "Quais são os pré-requisitos da disciplina Pesquisa Operacional II na Engenharia de Produção em Patos, currículo 2021?" # ToolCall - OK
question = "É necessário cursar alguma disciplina antes de Logística na Engenharia de Produção no campus de Patos, currículo 2021?" # ToolCall - OK
question = "Quais disciplinas são pré-requisitos para Álgebra Linear II no curso de Matemática em Cuité?" # ToolCall - OK
question = "Preciso ter cursado alguma disciplina antes de me matricular em Cálculo Diferencial e Integral III na Matemática em Cuité?" # ToolCall - OK

# Turmas

question = "Quais turmas de Cálculo I existem no curso de Engenharia Civil em Campina Grande no período 2022.1 com currículo 2020?" # ToolCall - OK
question = "Quais turmas estão disponíveis para Física Geral I na Engenharia Mecânica no campus de Cajazeiras no período 2023.2?" # ToolCall - OK
question = "Quantas turmas existem da disciplina Álgebra Linear I no curso de Matemática em Sumé?" # ToolCall - OK
question = "Quais são as turmas de Estrutura de Dados na Ciência da Computação em Sousa?" # ToolCall - OK
question = "Quantas turmas de Bioquímica foram ofertadas para o curso de Engenharia de Alimentos no campus de Pombal no período 2021.1 com currículo 2019?" # ToolCall - OK
question = "Quais turmas existem da disciplina Programação I no curso de Engenharia de Computação?" # ToolCall - OK
question = "Quais turmas de Estatística estão disponíveis no curso de Ciencia da Computação no campus de Patos?" # ToolCall - OK
question = "Quais turmas existem para a disciplina Probabilidade s no curso de Ciencia da Computação no campus de Campina Grande?" # ToolCall - OK
question = "Quais turmas existem da disciplina Cálculo II no curso de Engenharia de Produção no campus cajazeiras no período 2023.2?" # ToolCall - OK
question = "Quantas turmas existem da disciplina História da Educação no curso de Licenciatura em Pedagogia no campus de Cuité?" # ToolCall - OK
question = "Quais turmas existem para a disciplina Banco de Dados no curso de Tecnologia em Análise e Desenvolvimento de Sistemas em Sousa?" # ToolCall - OK
question = "Quais turmas de Cálculo Numérico estão disponíveis no curso de BSI em Campina Grande?" # ToolCall - OK
question = "Quais turmas existiam de Química Geral em Engenharia de Materiais no campus de Campina Grande no período 2017.1?" # ToolCall - OK
question = "Quais turmas foram ofertadas da disciplina Hidráulica no curso de Engenharia Ambiental e Sanitária em Patos?" # ToolCall - OK
question = "Quais turmas foram ofertadas para Tópicos Especiais em Computação no curso de Engenharia de Computação em Sousa com currículo 2021?" # ToolCall - OK
question = "Quais turmas existem da disciplina Empreendedorismo no curso de Administração no campus de Cajazeiras?" # ToolCall - OK
question = "Existe turma de Física Experimental II no campus de Campina Grande no curso de Física?" # ToolCall - OK
question = "Quantas turmas foram ofertadas de Introdução à Filosofia no curso de Filosofia em Sumé no período 2020.2?" # ToolCall errou, chamou get_disciplinas 
question = "Tem alguma turma de Geometria Analítica no curso de Matemática no campus de Patos com currículo 2018?" # ToolCall - OK
question = "Quais turmas estão cadastradas para a disciplina Sociologia do curso de Sociologia no campus de Cuité?" # ToolCall - OK
question = "Quantas turmas tem a disciplina de calculo 2 no curso de ciencia da computacao, campus de campina grande?" # ToolCall - OK
question = "Quantas turmas tem a disciplina de ciencia de dados preditiva no curso de ciencia da computacao, campus de campina grande?" # ToolCall - OK

agent.run(question=question)