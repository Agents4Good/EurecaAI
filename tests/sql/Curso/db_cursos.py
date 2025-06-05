import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
local = os.path.join(BASE_DIR, "Curso", "tabela.json")

def criar_banco():
    with open(local, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    nome_tabela = list(schema.keys())[0]
    colunas = schema[nome_tabela]

    colunas_sql = []
    for nome, props in colunas.items():
        tipo = props['type']
        colunas_sql.append(f'{nome} {tipo}')

    criar_tabela = f"""
    CREATE TABLE IF NOT EXISTS {nome_tabela} (
        {", ".join(colunas_sql)}
    )
    """

    conexao = sqlite3.connect('cursos.db')
    cursor = conexao.cursor()
    cursor.execute(criar_tabela)
    conexao.commit()
    conexao.close()
    print(f"Tabela {nome_tabela} criada com sucesso")


def inserir_dados(dados_a_inserir):
    try:
        with open(local, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        nome_tabela = list(schema.keys())[0]
        colunas = schema[nome_tabela]

        conexao = sqlite3.connect('cursos.db')
        cursor = conexao.cursor()

        nomes_colunas = list(colunas.keys())
        placeholders = ', '.join(['?'] * len(nomes_colunas))
        sql_insert = f"""
        INSERT INTO {nome_tabela} ({', '.join(nomes_colunas)})
        VALUES ({placeholders})
        """

        for item in dados_a_inserir:
            valores = [item.get(coluna, None) for coluna in nomes_colunas]
            cursor.execute(sql_insert, valores)

        conexao.commit()
        conexao.close()
        print(f"{len(dados_a_inserir)} registros inseridos na tabela {nome_tabela}")
    except Exception as error:
        print("Erro ao inserir dados:", error)


def recuperar_dados():
    try:
        nome_tabela = 'Curso'
        conexao = sqlite3.connect('cursos.db')
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()

        cursor.execute(f"SELECT * FROM {nome_tabela}")
        linhas = cursor.fetchall()
        conexao.close()

        dados = [dict(linha) for linha in linhas]
        print("Dados recuperados com sucesso")
        return dados
    except Exception as error:
        print("Erro ao recuperar dados:", error)
        return []