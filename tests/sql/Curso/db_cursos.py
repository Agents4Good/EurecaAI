import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
local = os.path.join(BASE_DIR, "", "Curso", "tabela.json")

def inserir_dados(dados_a_inserir):
    try:
        with open(local, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        nome_tabela = list(schema.keys())[0]
        colunas = schema[nome_tabela]

        dados = dados_a_inserir

        conexao = sqlite3.connect('cursos.db')
        cursor = conexao.cursor()

        nomes_colunas = list(colunas.keys())
        placeholders = ', '.join(['?'] * len(nomes_colunas))
        sql_insert = f"""
        INSERT INTO {nome_tabela} ({', '.join(nomes_colunas)})
        VALUES ({placeholders})
        """

        for item in dados:
            valores = [item.get(coluna, None) for coluna in nomes_colunas]
            cursor.execute(sql_insert, valores)

        conexao.commit()
        conexao.close()
        print(f"{len(dados)} registros inseridos na tabela {nome_tabela}")
    except Exception as error:
        print(error)


def recuperar_dados():
    try:
        nome_tabela = 'Curso'

        conexao = sqlite3.connect('cursos.db')
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()

        cursor.execute(f"SELECT * FROM {nome_tabela}")
        linhas = cursor.fetchall()

        dados = [dict(linha) for linha in linhas]

        conexao.close()
        print("Dados recuperados com sucesso")
        return dados
    except Exception as error:
        print(error)