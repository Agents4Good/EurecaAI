import sqlite3
import json
import os
from typing import TypedDict
from .SQLGeneratorVanna import SQLGeneratorVanna
from .LLMGenerateSQL import LLMGenerateSQL
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from langchain_google_genai import ChatGoogleGenerativeAI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class CleanQuestion(TypedDict):
    question: str

class GerenciadorSQLAutomatizado:
    def __init__ (self, table_name, db_name, prompt, temperature: float = 0):
        self.table_name = table_name
        self.temperature = temperature
        self.db_name = db_name
        self.path = os.path.join(BASE_DIR, "", self.table_name, "tabela.json")
        print(f"Path do arquivo JSON: {self.path}")   
             
        if not os.path.exists(self.path):
            raise ValueError("Arquivo JSON não encontrado. Verifique o caminho do arquivo.")
        
        self.table_info = self.__create_table()
        self.prompt = prompt

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

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_info}")
        cursor.execute(f"DELETE FROM {self.table_name}")

        dados = self._extract_campus()
        for dado in data_json:
            valores_processados = []
            for campo in dados:
                valor = dado.get(campo)
                # Se for uma lista, converte para a string com delimitadores
                if isinstance(valor, list):
                    valor = "," + ",".join(str(v) for v in valor) + ","
                valores_processados.append(valor)

            cursor.execute(f"""
            INSERT OR IGNORE INTO {self.table_name} VALUES ({', '.join(['?' for _ in dados])})
            """, tuple(valores_processados))

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
        
    
    def __clean_question(self, question: str):
        """
            Limpa a pergunta removendo os resíduos.

            Args:
                question (str): A pergunta a ser limpa.
            Returns:
                str: A pergunta limpa.
        """

        model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0.0)

        prompt = f"""
        Você é um assistente de IA especializado em limpar perguntas de usuários.
        Sua tarefa é **reformular** a pergunta original, removendo apenas os trechos que forem desconexos, redundantes ou que não agreguem sentido (ex: "no ano", "do campus", "do curso") **somente se estiverem mal encaixados ou sem sentido na frase**.

        👉 **Regras**:
        1. Analise a “Pergunta original” e identifique preposições ou fragmentos que criem quebras de contexto.  
        2. Remova esses fragmentos, mantendo apenas o núcleo da pergunta.  
        3. Remova também palavras que não fazem sentido ou que não agregam valor à pergunta.
        4. Não adicione informações ou faça suposições sobre o que o usuário quis dizer.
        5. Retorne **apenas** a “Pergunta limpa”, sem comentários, explicações ou markup adicional.

        **Pergunta original:**
        {question}
        """

        structured_output = model.with_structured_output(CleanQuestion)
        response = structured_output.invoke(prompt)

        if response['question']:
            print("Pergunta limpa: ", response['question'])
            return response['question']
        else:
            raise ValueError("Erro ao limpar a pergunta.")
      
    
    
    def get_data(self, embbedings:str, question: str, clean_question: bool = False):
        if clean_question:
            question = self.__clean_question(question)
       
        #O qwen3 precisa de regex
        #sqlgen = SQLGeneratorVanna(LLM=ChatOllama, model_name=embbedings, db_path=self.db_name, config={'model': 'llama3.1', 'temperature': self.temperature, "max_tokens": 512, "initial_prompt": self.prompt})

        sqlgen = SQLGeneratorVanna(LLM=ChatDeepInfra, model_name=embbedings, db_path=self.db_name, config={'model': 'meta-llama/Llama-3.3-70B-Instruct', 'temperature': self.temperature, "max_tokens": 512, "initial_prompt": self.prompt})

        #sqlgen = SQLGeneratorVanna(LLM=ChatGoogleGenerativeAI, model_name=embbedings, db_path=self.db_name, config={'model': 'gemini-2.0-flash', 'temperature': self.temperature, "max_tokens": 512, "initial_prompt": self.prompt})
       

        sql = sqlgen.generate_sql(question=question)
    
        print("\n=============================================\n")
        print(f"Query gerada: {sql}")
        print("\n=============================================\n")

        result = self.__execute_sql(sql)
        return  result

    
