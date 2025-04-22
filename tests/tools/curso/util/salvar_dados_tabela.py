from faker import Faker
faker = Faker('pt_BR')
import sqlite3
from .tabelas import TABELA_CURSO, TABELA_ESTUDANTE_CURSO

def save_cursos(data_json, db_name):
    """Salva os dados dos cursos temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos cursos temporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(TABELA_CURSO)
    cursor.execute("DELETE FROM Curso")

    for curso in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO Curso VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            curso["codigo_do_curso"],
            curso["descricao"],
            curso["grau_do_curso"],
            curso["codigo_do_setor"],
            curso["nome_do_setor"],
            curso["campus"],
            curso["nome_do_campus"],
            curso["turno"],
            curso["periodo_de_inicio"],
            curso["data_de_funcionamento"].split(" ")[0] if curso["data_de_funcionamento"] else "00-00-0000",
            curso["codigo_inep"],
            curso["modalidade_academica"],
            curso["curriculo_atual"],
            curso["area_de_retencao"],
            curso['ciclo_enade']
        ))

    conn.commit()
    conn.close()


def save_estudantes_cursos(data_json, db_name):
    """Salva os dados dos estudantes dos cursos temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos estudantes dos cursos temporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(TABELA_ESTUDANTE_CURSO)
    cursor.execute("DELETE FROM Estudante")

    for estudante in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO Estudante VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            faker.name(),
            estudante["matricula_do_estudante"],
            estudante["nome_do_curso"],
            estudante["turno_do_curso"],
            estudante["codigo_do_curriculo"],
            estudante["nome_do_campus"],
            estudante["estado_civil"],
            estudante["sexo"],
            estudante["situacao"],
            estudante["motivo_de_evasao"],
            estudante["periodo_de_evasao"],
            estudante["forma_de_ingresso"],
            estudante["periodo_de_ingresso"],
            estudante["nacionalidade"],
            estudante["local_de_nascimento"],
            estudante["naturalidade"],
            estudante["cor"],
            estudante["ano_de_conclusao_ensino_medio"],
            estudante["tipo_de_ensino_medio"],
            estudante["politica_afirmativa"],
            estudante["cra"],
            estudante["mc"],
            estudante["iea"],
            estudante["periodos_completados"],
            estudante["prac_atualizado"],
            estudante["prac_renda_per_capita_ate"],
            "Sim" if len(estudante["deficiencias"]) > 0 else "Não"
        ))
    conn.commit()
    conn.close()