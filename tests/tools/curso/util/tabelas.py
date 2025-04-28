TABELA_CURSO = """
Curso (
    codigo_do_curso INTEGER, -- Codigo do curso (ID: chave primária)
    nome_do_curso Text, -- Nome do curso
    codigo_do_setor INTEGER, -- Código do setor ao qual o curso pertence
    nome_do_setor Text, -- Nome do setor ao qual o curso pertence
    nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal".
    turno Text, -- Turno do curso pode ser "Matutino", "Vespertino", "Noturno", "Integral" e "Diurno"
    periodo_de_inicio REAL, -- período em que o curso foi criado/fundado (exemplo: 2010.1, 1998.2)
    ano_de_criacao_do_curso Text, -- Ano em que o curso foi criado/fundado
    codigo_inep INTEGER, -- Código INEP do curso 
    modalidade_academica Text, -- ENUM cuja as opções são: "BACHARELADO", "LICENCIATURA", "TECNICO".
    curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada
    ciclo_enade INTEGER -- De quantos em quantos semestres ocorre a prova do enade 
);
"""

