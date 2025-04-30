import sqlite3
from .tabela_disciplina import TABELA_SQL_DISCIPLINA

def save_disciplinas(data_json, db_name):
    """Salva as disciplinas temporariamente em um banco de dados SQLite."""
    print("Salvando dados dos estudantes de uma disciplina emporariamente em um banco de dados SQLite")

    conn = sqlite3.connect(db_name)
    print("conectado")
    cursor = conn.cursor()
    cursor.execute(TABELA_SQL_DISCIPLINA)
    cursor.execute("DELETE FROM Disciplina")
    
    print("\n\n\n\n\n", data_json)
    for disciplina in data_json:
        cursor.execute("""
        INSERT OR IGNORE INTO Disciplina VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                disciplina["codigo_da_disciplina"],
                disciplina["nome"],
                disciplina["carga_horaria_teorica_semanal"],
                disciplina["carga_horaria_pratica_semanal"],
                disciplina["quantidade_de_creditos"],
                disciplina["horas_totais"],
                disciplina["media_de_aprovacao"],
                disciplina["carga_horaria_teorica_minima"],
                disciplina["carga_horaria_pratica_minima"],
                disciplina["carga_horaria_teorica_maxima"],
                disciplina["carga_horaria_pratica_maxima"],
                disciplina["numero_de_semanas"],
                disciplina["codigo_do_setor"],
                disciplina["carga_horaria_extensao"]
        ))
    conn.commit()
    conn.close()