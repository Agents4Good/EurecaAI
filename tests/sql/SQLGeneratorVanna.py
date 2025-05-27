#from vanna.ollama import Ollama
import re
from vanna.vannadb import VannaDB_VectorStore
from .CustomLLMVanna import MyCustomLLmVanna
from dotenv import load_dotenv
load_dotenv()

import os

load_dotenv()
VANNA_API_KEY_VECTORSTORE = os.getenv('VANNA_API_KEY_VECTORSTORE')


class MyVanna(VannaDB_VectorStore, MyCustomLLmVanna):
    def __init__(self, LLM, model_name: str,  config=None):
        MY_VANNA_MODEL = model_name
        VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key=VANNA_API_KEY_VECTORSTORE, config=config,)
        MyCustomLLmVanna.__init__(self, LLM, config=config)

    def get_sql_prompt(
        self,
        initial_prompt: str,
        question: str,
        question_sql_list: list,
        ddl_list: list,
        doc_list: list,
        **kwargs
    ):
        if initial_prompt is None:
            initial_prompt = f"You are a {self.dialect} expert. " + \
            "Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the format instructions. "

        # Adiciona DDL ao prompt
        initial_prompt = self.add_ddl_to_prompt(
            initial_prompt, ddl_list, max_tokens=self.max_tokens
        )

        # Adiciona documentação estática, se houver
        if self.static_documentation != "":
            doc_list.append(self.static_documentation)

        # Adiciona documentação ao prompt
        initial_prompt = self.add_documentation_to_prompt(
            initial_prompt, doc_list, max_tokens=self.max_tokens
        )

        # >>>> Removido: trecho que adicionava os "Response Guidelines"
        message_log = [self.system_message(initial_prompt)]

        for example in question_sql_list[:2]:  # Limita a 3 exemplos
            if example is None:
                print("example is None")
            else:
                if "question" in example and "sql" in example:
                    message_log.append(self.user_message(example["question"]))
                    message_log.append(self.assistant_message(example["sql"]))

        message_log.append(self.user_message(question))

        return message_log


class SQLGeneratorVanna:
    def __init__(self, LLM,  model_name: str = "your-model", db_path: str = None, config=None):
        self.vanna = MyVanna(LLM, model_name=model_name, config=config)
        
        if db_path:
            self.vanna.connect_to_sqlite(db_path)
        
        #training_data = self.vanna.get_training_data()
        #if training_data.empty:
        self._train_ddl()

    def generate_sql(self, question: str, visualize: bool = False, print_results: bool = False, allow_llm_to_see_data: bool = False):
        """
        Gera o SQL a partir da pergunta.
        :param question: Pergunta a ser feita.
        :param visualize: Se True, visualiza o SQL gerado.
        :param print_results: Se True, imprime os resultados do SQL.
        :param allow_llm_to_see_data: Se True, permite que o LLM veja os dados.
        :return: SQL gerado.
        """
    
        resposta = self.vanna.generate_sql(question=question, visualize=visualize, print_results=print_results, allow_llm_to_see_data=allow_llm_to_see_data)
       
        return resposta
        
    def _train_ddl(self):
        """
        Treina o modelo com o DDL do banco de dados.
        Só precisa ser executado uma vez para cada agente.
        :return: None
        """
        df_ddl = self.vanna.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
        for ddl in df_ddl['sql'].to_list():
            self.vanna.train(ddl=ddl)
    
    def __getattr__(self, name):
        # Qualquer método não encontrado será procurado em self.vanna
        return getattr(self.vanna, name)

    


# O MODELO PRECISA ESTAR DISPONIVEL  NO OLLAMA e BAIXADO NO SEU COMPUTADOR
# vn = MyVanna(model_name="curso", config={'model': 'llama3.1', 'temperature': 0.0})
# vn.connect_to_sqlite('db_cursos.sqlite')


# #TREINA O MODELO COM O DDL DO BANCO, DEVE SER EXECUTADO APENAS UMA VEZ
# df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
# for ddl in df_ddl['sql'].to_list():
#     vn.train(ddl=ddl)


# vn.train(
#     question= "Qual o código do curso de ciência da computação?",
#     sql= "SELECT codigo_do_curso FROM Curso",
# )

# vn.train(
#     question= "Traga todos os cursos da uasc",
#     sql = "SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'UNID. ACAD. DE SISTEMAS E COMPUTAÇÃO'",
# )

# vn.train(
#     question = "Traga todos os cursos da unidade acadêmica de sistemas e computação",
#     sql = "SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'UNID. ACAD. DE SISTEMAS E COMPUTAÇÃO'",
# )

# vn.train(
#     question= "Quais os cursos do campus de campina grande?",
#     sql= "SELECT nome_do_curso FROM Curso",
# )

# vn.train(
#     question="Quais os cursos bacharelados da uasc?",
#     sql="SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'UNID. ACAD. DE SISTEMAS E COMPUTAÇÃO' AND modalidade_academica = 'BACHARELADO'",
# )

# vn.train(
#     question= "Quais os cursos do cct do campus campina grande?",
#     sql= "SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'CCT - CENTRO DE CIÊNCIAS E TECNOLOGIA'",
# )

# vn.train(
#     question="Quais os cursos do ccbs do campus campina grande?",
#     sql="SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'CCBS - CENTRO DE CIÊNCIAS BIOLÓGICAS E DA SAÚDE'",
# )

# vn.train(
#     question= "traga todos os cursos do ch",
#     sql= "SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'CH - CENTRO DE HUMANIDADES'",
# )

# vn.train(
#     question= "Traga todos os cursos do centro de engenharia elétrica e informática",
#     sql= "SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'CEEI - CENTRO DE ENGENHARIA ELÉTRICA E INFORMÁTICA'",
# )

# vn.train(
#     question="Quais os cursos do ceei?",
#     sql="SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'CEEI - CENTRO DE ENGENHARIA ELÉTRICA E INFORMÁTICA'",
# )

# vn.train(
#     question= "Traga os cursos relacionados ao ceei",
#     sql= "SELECT codigo_do_curso, nome_do_curso FROM Curso WHERE nome_do_setor = 'CEEI - CENTRO DE ENGENHARIA ELÉTRICA E INFORMÁTICA'",
# )


# vn.train(
#     question = "código do cursos do cct",
#     sql = "SELECT codigo_do_curso FROM Curso WHERE nome_do_setor = 'CCT - CENTRO DE CIÊNCIAS E TECNOLOGIA'",
# )

# response = vn.generate_sql("Quero informações dos cursos do ceei", visualize=False, print=False, allow_llm_to_see_data=False)
# print()
# print()
# print("=====================================")
# print("SQL ", vn.generate_sql("nome dos cursos do cct", visualize=False, print_results=False, allow_llm_to_see_data=True))
# print("=====================================")
# #print(vn.run_sql(vn.extract_sql(response)))
# print("=====================================")

#GERA O SQL E RETORNA O RESULTADO
#resposta = vn.ask("De onde vem os estudantes do curso de ciência da computação do campus Campina grande por estado? Me mostre pra cada estado do país", visualize=False, print_results=False, allow_llm_to_see_data=True)

# GERA SOMENTE O SQL
#teste = vn.generate_sql("De onde vem os estudantes do curso de ciência da computação do campus Campina grande por estado? Me mostre pra cada estado do país", visualize=False, print_results=False, allow_llm_to_see_data=True)



# # TREINANDO O MODELO COM UMA PERGUNTA E SQL
# vn.train(
#     question="Traga os cursos do ceei",
#     sql="SELECT nome_do_curso FROM Curso WHERE nome_do_setor = 'CEEI - CENTRO DE ENGENHARIA ELÉTRICA E INFORMÁTICA'",
# )


#vn.remove_training_data(id='1-ddl')

# print("=====================================")
# #print("SIMILARES ",vn.get_similar_question_sql("Quero cursos do ceei"))

# auxiliar = vn.get_training_data()
# print("=====================================")
# print("DADOS TREINADOS: ", auxiliar)
# print("=====================================")
# print("SQL GERADO ", resposta[0])
# print("=====================================")
# print("RESULTADO DO SQL: ", resposta[1])


# print("=====================================")
# print("SQL GERADO TESTE:", vn.extract_sql(teste))
# print("=====================================")

# conectar_e_executar_query('db_estudantes.sqlite', """
# SELECT naturalidade, COUNT(*) FROM Estudante_Info_Gerais GROUP BY naturalidade
# """)


# !pip install vanna


# from vanna.remote import VannaDefault
# vn = VannaDefault(model='curso', api_key='775904ea08214218a60ac82a0d106877', config={'model': 'llama3.1', 'temperature': 0.0})
# vn.connect_to_sqlite('db_cursos.sqlite') # Connect to your database here

# # resposta = vn.ask("Quais são os cursos do campus de campina grande?", visualize=False, print_results=True, allow_llm_to_see_data=True)

# # print("=====================================")
# # print("SQL GERADO: ", resposta)
# # print("=====================================")

# df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
# for ddl in df_ddl['sql'].to_list():
#     vn.train(ddl=ddl)

# from vanna.flask import VannaFlaskApp

# VannaFlaskApp(vn, allow_llm_to_see_data=True).run()







