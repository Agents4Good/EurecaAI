from .generate_sql import LLMGenerateSQL
from .execute_sql import execute_sql

def obter_dados_sql(query: str, db_name: str, PROMPT, TABELA, temperature = 0) -> list:
    print("Obtendo dados via consulta SQL")
    #sqlGenerateLLM = LLMGenerateSQL(model="llama3.1:8b-instruct-q5_K_M", prompt=PROMPT)
    sqlGenerateLLM = LLMGenerateSQL(model="meta-llama/Meta-Llama-3.1-8B-Instruct", prompt=PROMPT)
    result = sqlGenerateLLM.write_query(query=query, tabela=TABELA)

    result = execute_sql(result['query'], db_name)

    print("Devolvendo resultado do comand SQL:", result)
    return result