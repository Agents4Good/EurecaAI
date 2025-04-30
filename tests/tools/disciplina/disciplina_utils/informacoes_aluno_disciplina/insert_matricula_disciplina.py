from faker import Faker
faker = Faker('pt_BR')
import sqlite3
from .tabela_matricula_disciplina import TABELA_ESTUDANTE_DISCIPLINA

def save_estudante_disciplinas(data_json, db_name):
    """Salva as disciplinas temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos estudantes de uma disciplina emporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(TABELA_ESTUDANTE_DISCIPLINA)
    cursor.execute("DELETE FROM EstudanteDisciplina")
    
    for disciplina in data_json:
        Faker.seed(int(disciplina["matricula_do_estudante"]))
        cursor.execute("""
        INSERT OR IGNORE INTO EstudanteDisciplina (
            nome_do_estudante, matricula_do_estudante, status, media_final, dispensou
        ) VALUES (?, ?, ?, ?, ?)
        """, (
            faker.name(),
            disciplina["matricula_do_estudante"],
            "Reprovado por Nota" if disciplina["status"] == "Reprovado" else disciplina["status"],
            disciplina["media_final"] if type(disciplina["media_final"]) == float else 0,
            "Sim" if (disciplina["dispensas"] and len(disciplina["dispensas"] > 0)) else "Não"
        ))
    conn.commit()
    conn.close()