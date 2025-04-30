TABELA_DISCIPLINA = """
CREATE TABLE IF NOT EXISTS Disciplina (
    codigo_da_disciplina INTEGER, -- Código da disciplina;
    nome TEXT, -- Nome da disciplina;
    carga_horaria_teorica_semanal INTEGER, -- Número de horas de aula teoricas dadas na semana;
    carga_horaria_pratica_semanal INTEGER, -- Número de horas de aula teóricas dadas na semana;
    quantidade_de_creditos INTEGER,
    horas_totais INTEGER,
    media_de_aprovacao INTEGER,
    carga_horaria_teorica_minima INTEGER,
    carga_horaria_pratica_minima INTEGER,
    carga_horaria_teorica_maxima INTEGER,
    carga_horaria_pratica_maxima INTEGER,
    numero_de_semanas INTEGER,
    codigo_do_setor INTEGER,
    nome_do_setor TEXT,
    campus INTEGER,
    nome_do_campus TEXT,
    status TEXT,
    contabiliza_creditos TEXT,
    tipo_de_componente_curricular TEXT,
    carga_horaria_extensao INTEGER
);
"""