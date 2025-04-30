import sqlite3
import json
import os

from .LLMGenerateSQL import LLMGenerateSQL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script atual

PROMPT_SQL_CURSOS = '''
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - codigo_do_curso
  - nome_do_curso
  - codigo_do_setor
  - nome_do_setor
  - nome_do_campus
  - turno
  - periodo_de_inicio
  - ano_de_criacao_do_curso
  - codigo_inep
  - modalidade_academica
  - curriculo_atual
  - ciclo_enade
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
- Gere o SQL no formato correto, apenas o SQL e mais nada.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
'''



class GerenciadorSQLAutomatizado:
    def __init__ (self, table_name, db_name):
        self.table_name = table_name
        self.db_name = db_name
        self.path = os.path.join(BASE_DIR, "", self.table_name, "tabelas.json") #GAMBIARRA PRA FUNCIONAR

        print(f"Path do arquivo JSON: {self.path}")        
        if not os.path.exists(self.path):
            raise ValueError("Arquivo JSON não encontrado. Verifique o caminho do arquivo.")
        
        self.tabela = self.__create_table()

    def __create_table(self):
        """
        Cria uma tabela no banco de dados com base na definição fornecida.

        Args:
            tabela (str): O nome da tabela no arquivo json.

        Returns:
            str: TABELA gerada no formato 
            TABELA (
                coluna1 tipo -- descrição,
                coluna2 tipo, -- descrição,
                ...
            );
        """

        with open(self.path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Erro ao carregar o arquivo JSON: {e}")


        if self.table_name not in data:
            raise ValueError(f"A tabela '{self.table_name}' não foi encontrada no arquivo JSON.")

        sql = f"{self.table_name}(\n"
        qtd = len(data[self.table_name])
        c = 0
        for column, column_type in data[self.table_name].items():
            if (c == qtd - 1):
                sql += f"{column} {column_type['type']} -- {column_type['description']}\n"
            else:
                sql += f"{column} {column_type['type']}, -- {column_type['description']}\n"
            c+=1
            #print(f"Coluna: {column}, Tipo: {column_type['type']} , DESC: {column_type['description']} \n\n")

        sql += ");"        
        return sql

    def __extract_campus(self):
        """
            Extrai os campos mapper da tabela especificada no arquivo JSON.
            ex: nome_do_curso é mapeado para descricao

            Returns:
                list: Uma lista de campos mapeados da tabela.
        """

        with open(self.path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Erro ao carregar o arquivo JSON: {e}")
        
        # Verifica se a tabela existe no JSON
        if self.table_name not in data:
            raise ValueError(f"A tabela '{self.table_name}' não foi encontrada no arquivo JSON.")
        
        campus_tabela = []
        for column, column_type in data[self.table_name].items():
            campus_tabela.append(column_type['mapper'])

        return campus_tabela

    def save_data(self, data_json):
        """
            Salva os dados no banco de dados.

            Args:
                data_json (list): Lista de dicionários com os dados.
        """
       
        print("Salvando dados dos cursos temporariamente em um banco de dados SQLite")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.tabela}")
        cursor.execute(f"DELETE FROM {self.table_name}")

        dados = self.__extract_campus()
        for dado in data_json:
            cursor.execute(f"""
            INSERT OR IGNORE INTO {self.table_name} VALUES ({', '.join(['?' for _ in dados])})
            """, tuple(dado[campo] for campo in dados))

        conn.commit()
        conn.close()
        print(f"Dados salvos na tabela {self.table_name} do banco de dados {self.db_name}.")


    def __execute_sql(self, sql: str):
        """
            Executa uma consulta SQL no banco de dados.

            Args:
                query (str): A consulta SQL a ser executada
            Returns:
                list: Lista de resultados da consulta.
        """
        print("Executando o comando SQL")

        print("SQL gerado:", sql)
        conn = sqlite3.connect(self.db_name)
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
    
    def get_data(self, query: str, prompt, temperature=0):
        sqlGenerateLLM = LLMGenerateSQL(model="llama3.1:8b-instruct-q5_K_M", prompt=prompt)
        #sqlGenerateLLM = LLMGenerateSQL(model="meta-llama/Meta-Llama-3.1-8B-Instruct", prompt=prompt)
        result = sqlGenerateLLM.write_query(query=query, tabela=self.tabela)
        print(f"Query gerada: {result['query']}")
        try:
            result = self.__execute_sql(result['query'])
        except:
            if (temperature < 0.5):
                result = self.get_data(query,prompt, temperature + 0.1)
            return "Error: Não conseguimos achar os dados perguntados pelo usuário!"

        print("Devolvendo resultado do comand SQL:", result)
        return result
    

# g = GerenciadorSQLAutomatizado("Curso", "db_cursos.sqlite")
# g.save_data(
#     [
#         {
#             "codigo_do_curso": 123456,
#             "descricao": "Engenharia de Computação",
#             "codigo_do_setor": 2323,
#             "nome_do_setor": "Computação",
#             "nome_do_campus": "Campina Grande",
#             "turno": "Diurno",
#             "periodo_de_inicio": 2010,
#             "codigo_inep": 123456,
#             "modalidade_academica": "Bacharelado",
#             "curriculo_atual": 2020,
#             "ciclo_enade": 2021
#         },
#         {
#             "codigo_do_curso": 789808,
#             "descricao": "Engenharia de Alimentos",
#             "codigo_do_setor": 2323,
#             "nome_do_setor": "Alimentos",
#             "nome_do_campus": "Campina Grande",
#             "turno": "Diurno",
#             "periodo_de_inicio": 2010,
#             "codigo_inep": 123456,
#             "modalidade_academica": "Bacharelado",
#             "curriculo_atual": 2020,
#             "ciclo_enade": 2021
#         }
#     ])


# print(g.get_data("Quantos cursos são oferecidos em Campina Grande?", PROMPT_SQL_CURSOS))

    


