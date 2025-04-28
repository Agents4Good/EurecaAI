
# TABELA_ESTUDANTE_CURSO = """
# Estudante (
#     nome_do_estudante TEXT, -- nome do estudante
#     matricula_do_estudante TEXT,
#     turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
#     codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
#     estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
#     sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
#     forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
#     nacionalidade TEXT, -- ENUM que pode ser "Brasileira" ou "Estrangeira".
#     local_de_nascimento TEXT, -- Nome da cidade onde nasceu.
#     naturalidade TEXT, -- Sigla do estado do estudante.
#     cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
#     deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
#     ano_de_conclusao_ensino_medio INTEGER, 
#     tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
#     cra REAL, -- Coeficiente de rendimento acadêmico.
#     mc REAL, -- Média de conclusão de curso.
#     iea REAL, --Indice de eficiência acadêmica.
#     periodos_completados INTEGER, 
#     prac_renda_per_capita_ate INTEGER -- Renda mensal da família em salários mínimos.
# );
# """

TABELA_ESTUDANTE_CURSO_INFO_GERAIS = """
EstudanteGeral (
    nome_do_estudante TEXT, -- nome do estudante
    matricula_do_estudante TEXT, -- matricula do estudante
    idade INTEGER, -- idade do estudante.
    estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
    sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
    cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
    nacionalidade TEXT, -- ENUM que pode ser "Brasileira" ou "Estrangeira".
    local_de_nascimento TEXT, -- Nome da cidade onde nasceu.
    naturalidade TEXT -- Sigla do estado do estudante.
    deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
    prac_renda_per_capita_ate INTEGER -- Renda mensal da família em salários mínimos.
)
"""

TABELA_ESTUDANTE_CURSO_INFO_ESPECIFICAS = """
EstudanteCurso (
    nome_do_estudante TEXT, -- nome do estudante
    matricula_do_estudante TEXT, -- matricula do estudante
    turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
    codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
    forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
    ano_de_conclusao_ensino_medio INTEGER, 
    tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
    cra REAL, -- Coeficiente de rendimento acadêmico.
    mc REAL, -- Média de conclusão de curso.
    iea REAL, --Indice de eficiência acadêmica.
    periodos_completados INTEGER -- Quantidade de periodos que o estudante já completou.
)
"""


