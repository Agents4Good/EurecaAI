from .GerenciadorSQLAutomatizado import LLMGenerateSQL
from .execute_sql import execute_sql

def obter_dados_sql(query: str, db_name: str, LLM, model, PROMPT, TABELA, temperature = 0):
    print("Obtendo dados via consulta SQL")
    sqlGenerateLLM = LLMGenerateSQL(LLM=LLM, model=model, prompt=PROMPT)
    result = sqlGenerateLLM.write_query(query=query, tabela=TABELA)

    try:
        result = execute_sql(result['query'], db_name)
    except:
        if (temperature < 0.5):
            result = obter_dados_sql(query, db_name, PROMPT, TABELA, temperature + 0.1)
        return "Error: Não conseguimos achar os dados perguntados pelo usuário!"
    
    print("Devolvendo resultado do comand SQL:", result)
    return result