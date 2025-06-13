import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
local = os.path.join(BASE_DIR, "", "", "tabela.json")

def inserir_dados(dados_a_inserir):
    try:
        with open(local, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        nome_tabela = list(schema.keys())[0]
        print(nome_tabela)
        colunas = schema[nome_tabela]

        conexao = sqlite3.connect('db_todos_cursos.sqlite')
        cursor = conexao.cursor()

        #nomes_colunas = list(colunas.keys())
        nomes_colunas = [coluna['mapper'] for coluna in colunas.values()]
        tipos_colunas = [coluna['type'] for coluna in colunas.values()]
        sql_create_table = f"""
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            {', '.join([f"{coluna} {tipo}" for coluna, tipo in zip(nomes_colunas, tipos_colunas)])}
        );
        """
        cursor.execute(sql_create_table)

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
    except Exception as e:
        conexao.close()
        return e


def recuperar_dados():
    try:
        nome_tabela = 'Curso'

        conexao = sqlite3.connect('db_todos_cursos.sqlite')
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()

        cursor.execute(f"SELECT * FROM {nome_tabela}")
        linhas = cursor.fetchall()

        dados = [dict(linha) for linha in linhas]

        conexao.close()
        print("Dados recuperados com sucesso")
        return dados
    except Exception as e:
        conexao.close()
        return str(e)