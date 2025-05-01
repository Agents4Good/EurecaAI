TABELA_SQL_DISCIPLINA = """
CREATE TABLE IF NOT EXISTS Disciplina (
    codigo_da_disciplina INTEGER, -- Identificador único da disciplina
    nome TEXT, -- Nome da disciplina
    carga_horaria_teorica_semanal INTEGER, -- Horas semanais de aulas teóricas
    carga_horaria_pratica_semanal INTEGER, -- Horas semanais de aulas práticas
    quantidade_de_creditos INTEGER, -- Créditos da disciplina (horas semanais lecionadas)
    horas_totais INTEGER, -- Total de horas da disciplina durante o curso
    media_de_aprovacao INTEGER, -- Média de estudantes aprovados na disciplina
    carga_horaria_teorica_minima INTEGER, -- Horas mínimas semanais de aulas teóricas
    carga_horaria_pratica_minima INTEGER, -- Horas mínimas semanais de aulas práticas
    carga_horaria_teorica_maxima INTEGER, -- Horas máximas semanais de aulas teóricas
    carga_horaria_pratica_maxima INTEGER, -- Horas máximas semanais de aulas práticas
    numero_de_semanas INTEGER, -- Número de semanas da disciplina
    codigo_do_setor INTEGER, -- Código do setor responsável pela disciplina
    carga_horaria_extensao INTEGER -- Horas da disciplina que contam como extensão
);
"""