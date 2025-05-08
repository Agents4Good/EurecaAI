import sqlite3
import json
import os
from .LLMGenerateSQL import LLMGenerateSQL
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from langchain_community.chat_models import ChatDeepInfra
BASE_DIR = os.path.dirname(os.path.abspath(__file__))





class GerenciadorSQLAutomatizado:
    def __init__ (self, table_name, db_name):
        self.table_name = table_name
        self.db_name = db_name
        self.path = os.path.join(BASE_DIR, "", self.table_name, "tabela.json")
        print(f"Path do arquivo JSON: {self.path}")   
             
        if not os.path.exists(self.path):
            raise ValueError("Arquivo JSON não encontrado. Verifique o caminho do arquivo.")
        
        self.tabela = self.__create_table()

    def __create_table(self):
        """
        Cria uma tabela no banco de dados com base na definição fornecida.

        Returns:
            str: TABELA gerada no formato 
            TABELA (
                coluna1 tipo -- descrição,
                coluna2 tipo -- descrição,
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

        linhas = []
        for column, column_type in data[self.table_name].items():
            linhas.append(f"{column} {column_type['type']}, -- {column_type['description']}")

        if linhas:
            linhas[-1] = linhas[-1].replace(',', '', 1)

        sql = f"{self.table_name}(\n" + "\n".join(linhas) + "\n);"
        return sql
       

    def _extract_campus_types_description(self):
        """
            Extrai os nomes dos campos, os tipos e a descrição no arquivo JSON.
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
            campus_tabela.append(f"{column} {column_type['type']} -- {column_type['description']}")

        return campus_tabela     

    def _extract_campus(self):
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

        dados = self._extract_campus()
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
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            conn.close()
            return [{"error": str(e)}]
    
    def get_data(self, query: str, prompt, temperature=0):
        #sqlGenerateLLM = LLMGenerateSQL(LLM=ChatDeepInfra, model="meta-llama/Meta-Llama-3.1-8B-Instruct", prompt=prompt)
        
        sqlGenerateLLM = LLMGenerateSQL(LLM=ChatOllama, model="qwen3:8b", prompt=prompt)
        result = sqlGenerateLLM.write_query(query=query, tabela=self.tabela)
        print(f"Query gerada: {result['query']}")
        try:
            result = self.__execute_sql(result['query'])
        except:
            if (temperature < 0.5):
                result = self.get_data(query,prompt, temperature + 0.1)
            return "Error: Não conseguimos achar os dados perguntados pelo usuário!"
        return result
    
