# teste para geração de SQL com o Vanna ai

from vanna.ollama import Ollama
from vanna.vannadb import VannaDB_VectorStore

import sqlite3

def conectar_e_executar_query(db_path, query):
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()

    try:
       
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            print("Resultados da consulta:")
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
        else:
            conexao.commit()
            print("Query executada com sucesso.")
    
    except sqlite3.Error as erro:
        print("Erro ao executar a query:", erro)
    
    finally:
        cursor.close()
        conexao.close()


API_KEY = "775904ea08214218a60ac82a0d106877"

class MyVanna(VannaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        MY_VANNA_MODEL = "eureca"
        VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key=API_KEY, config=config,)
        Ollama.__init__(self, config=config)

# O MODELO PRECISA ESTAR DISPONIVEL NO OLLAMA
vn = MyVanna(config={'model': 'llama3.1', 'temperature': 0.0})
vn.connect_to_sqlite('db_cursos.sqlite')


# TREINA O MODELO COM O DDL DO BANCO, DEVE SER EXECUTADO APENAS UMA VEZ
# df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
# for ddl in df_ddl['sql'].to_list():
#     vn.train(ddl=ddl)



#GERA O SQL E RETORNA O RESULTADO
resposta = vn.ask("Traga os cursos do setor uasc", visualize=False, print_results=False, allow_llm_to_see_data=True)

# GERA SOMENTE O SQL
teste = vn.generate_sql("Traga os cursos do setor uasc", visualize=False, print_results=False, allow_llm_to_see_data=True)


# # TREINANDO O MODELO COM UMA PERGUNTA E SQL
# vn.train(
#     question="Traga os cursos da UASC",
#     sql="SELECT nome_do_curso FROM Curso WHERE nome_do_setor = UNID. ACAD. DE SISTEMAS E COMPUTAÇÃO",
# )

print("=====================================")
#print("SIMILARES ",vn.get_similar_question_sql("Traga os cursos do setor unidade acadêmica de engenharia elétrica ", visualize=False, print_results=True, allow_llm_to_see_data=True))



auxiliar = vn.get_training_data()
print("=====================================")
print("DADOS TREINADOS: ", auxiliar)
print("=====================================")
print("SQL GERADO ", resposta[0])
print("=====================================")
print("RESULTADO DO SQL: ", resposta[1])


print("=====================================")
print("SQL GERADO TESTE:", teste)
print("=====================================")

conectar_e_executar_query('db_cursos.sqlite', """
SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'UNID. ACAD. DE SISTEMAS E COMPUTAÇÃO'
""")


# !pip install vanna

# from vanna.remote import VannaDefault
# vn = VannaDefault(model='chinook', api_key='775904ea08214218a60ac82a0d106877')
# vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')
# vn.ask('What are the top 10 artists by sales?')

# from vanna.flask import VannaFlaskApp
# VannaFlaskApp(vn).run()







