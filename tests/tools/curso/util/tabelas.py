TABELA_CURSO = """
CREATE TABLE IF NOT EXISTS Curso (
    codigo_do_curso INTEGER, -- Codigo do curso (ID: chave primária)
    nome_do_curso Text, -- Nome do curso
    codigo_do_setor INTEGER, -- Código do setor ao qual o curso pertence
    nome_do_setor Text, -- Nome do setor ao qual o curso pertence
    nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal".
    turno Text, -- Turno do curso pode ser "Matutino", "Vespertino", "Noturno", "Integral" e "Diurno"
    periodo_de_inicio REAL, -- período em que o curso foi criado/fundado
    data_de_funcionamento Text, -- Data em formato de Texto sobre quando o curso foi criado "YYYY-MM-DD" (usar esses zeros), deve converter em date
    codigo_inep INTEGER, -- Código INEP do curso 
    modalidade_academica Text, -- ENUM cuja as opções são: "BACHARELADO", "LICENCIATURA", "TECNICO".
    curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada
    ciclo_enade INTEGER -- De quantos em quantos semestres ocorre a prova do enade 
);
"""

TABELA_ESTUDANTE_CURSO = """
CREATE TABLE IF NOT EXISTS Estudante (
    nome_do_estudante TEXT, -- nome do estudante
    matricula_do_estudante TEXT,
    turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Vespertino", "Noturno" ou "Integral".
    codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
    estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
    sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
    forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
    nacionalidade TEXT, -- ENUM que pode ser "Brasileira" ou "Estrangeira".
    local_de_nascimento TEXT, -- Nome da cidade onde nasceu.
    naturalidade TEXT, -- Sigla do estado do estudante.
    cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
    deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
    ano_de_conclusao_ensino_medio INTEGER, 
    tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
    cra REAL, -- Coeficiente de rendimento acadêmico.
    mc REAL, -- Média de conclusão de curso.
    iea REAL, --Indice de eficiência acadêmica.
    periodos_completados INTEGER, 
    prac_renda_per_capita_ate REAL
);
"""
