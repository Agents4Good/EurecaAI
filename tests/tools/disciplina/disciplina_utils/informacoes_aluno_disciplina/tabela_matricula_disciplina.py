TABELA_DISCIPLINA = """
CREATE TABLE IF NOT EXISTS Estudante (
    nome_do_estudante TEXT, -- nome do estudante (nome de pessoa).
    matricula_do_estudante TEXT, -- Número de 9 digitos que representa o número da matrícula do estudante (usar se informou a matrícula do estudante).
    status TEXT, -- É um ENUM que representa a situação do estudante na disciplina. O ENUM pode ser "Aprovado", "Trancado", "Reprovado por Nota", "Reprovado por Falta". E quando peguntar apenas uma palavra próximo a reprovação sem especificar se foi por nota ou por falta use "Reprovado por Nota" OR Reprovado por Falta".
    media_final REAL, -- Nota do aluno na disciplina (usar se pedir informações de notas e médias).
    dispensou TEXT -- ENUM que pode ser "Sim" ou "Não". (usar se perguntar sobre dispensas).
);
"""