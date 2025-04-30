from faker import Faker
faker = Faker('pt_BR')
import sqlite3
from .tabelas import TABELA_CURSO

def save_cursos(data_json, db_name):
    """Salva os dados dos cursos temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos cursos temporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABELA_CURSO}")
    cursor.execute("DELETE FROM Curso")

    for curso in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO Curso VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            curso["codigo_do_curso"],
            curso["descricao"],
            curso["codigo_do_setor"],
            curso["nome_do_setor"],
            curso["nome_do_campus"],
            curso["turno"],
            curso["periodo_de_inicio"],
            f"{float(curso['periodo_de_inicio']):.0f}" if curso["periodo_de_inicio"] else "0",
            curso["codigo_inep"],
            curso["modalidade_academica"],
            curso["curriculo_atual"],
            curso['ciclo_enade']
        ))

    conn.commit()
    conn.close()
