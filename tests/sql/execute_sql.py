import sqlite3

def execute_sql(sql: str, db_name: str):
    print("Executando o comando SQL")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        print(f"Comando SQL executado:\n{sql}: {results}")
        return results
    except sqlite3.Error as e:
        conn.close()
        return [{"error": str(e)}]