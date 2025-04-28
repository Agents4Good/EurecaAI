import sqlite3
from faker import Faker
faker = Faker('pt_BR')
from .tabelas import *

# def save_estudantes_cursos(data_json, db_name):
#     """Salva os dados dos estudantes dos cursos temporariamente em um banco de dados SQLite."""
#     print("Salvando dados dos estudantes dos cursos temporariamente em um banco de dados SQLite")

#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABELA_ESTUDANTE_CURSO}")
#     cursor.execute("DELETE FROM Estudante")

#     for estudante in data_json:
#         cursor.execute("""
#         INSERT OR IGNORE INTO Estudante VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             faker.name(),
#             estudante["matricula_do_estudante"],
#             estudante["turno_do_curso"],
#             estudante["codigo_do_curriculo"],
#             estudante["estado_civil"],
#             estudante["sexo"],
#             estudante["forma_de_ingresso"],
#             estudante["periodo_de_ingresso"],
#             estudante["nacionalidade"],
#             estudante["local_de_nascimento"],
#             estudante["naturalidade"],
#             estudante["cor"],
#             estudante["ano_de_conclusao_ensino_medio"],
#             estudante["cra"],
#             estudante["mc"],
#             estudante["iea"],
#             estudante["periodos_completados"],
#             estudante["prac_renda_per_capita_ate"],
#             "Sim" if len(estudante["deficiencias"]) > 0 else "Não"
#         ))
#     conn.commit()
#     conn.close()
#     print("As informações dos estudantes foram todas salvas.")


def save_estudantes_cursos_info_gerais(data_json, db_name):
    """Salva os dados dos estudantes dos cursos temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos estudantes dos cursos temporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    #cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABELA_ESTUDANTE_CURSO_INFO_GERAIS}")
    cursor.execute(TABELA_ESTUDANTE_CURSO_INFO_GERAIS)
    cursor.execute("DELETE FROM EstudanteGeral")

    for estudante in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO EstudanteGeral VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            faker.name(),
            estudante["matricula_do_estudante"],
            estudante["idade"],
            estudante["estado_civil"],
            estudante["sexo"],
            estudante["cor"],
            estudante["nacionalidade"],
            estudante["local_de_nascimento"],
            estudante["naturalidade"],
            "Sim" if len(estudante["deficiencias"]) > 0 else "Não",
            estudante["prac_renda_per_capita_ate"]
        ))
    conn.commit()
    conn.close()
    print("As informações dos estudantes foram todas salvas.")


def save_estudantes_cursos_info_especificas(data_json, db_name):
    """Salva os dados dos estudantes dos cursos temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos estudantes dos cursos temporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABELA_ESTUDANTE_CURSO_INFO_ESPECIFICAS}")
    cursor.execute("DELETE FROM EstudanteCurso")

    for estudante in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO EstudanteCurso VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            faker.name(),
            estudante["matricula_do_estudante"],
            estudante["turno_do_curso"],
            estudante["codigo_do_curriculo"],
            estudante["forma_de_ingresso"],
            estudante["ano_de_conclusao_ensino_medio"],
            estudante["tipo_de_ensino_medio"],
            estudante["cra"],
            estudante["mc"],
            estudante["iea"],
            estudante["periodos_completados"]
        ))
    conn.commit()
    conn.close()
    print("As informações dos estudantes foram todas salvas.")