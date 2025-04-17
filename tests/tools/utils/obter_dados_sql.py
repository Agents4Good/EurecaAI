from ..utils.llm_genetate_sql import LLMGenerateSQL
from ..utils.execute_sql import execute_sql

def obter_dados_sql(query: str, db_name: str, PROMPT, TABELA, temperature = 0):
    print("\n\nObtendo dados via SQL")
    sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=PROMPT)
    result = sqlGenerateLLM.write_query(query=query, tabela=TABELA)
    print(result, "\n\n")

    try:
        result = execute_sql(result['query'], db_name)
    except:
        if (temperature < 0.5):
            result = obter_dados_sql(query, db_name, PROMPT, TABELA, temperature + 0.1)
        return "Error: Não conseguimos achar os dados perguntados pelo usuário!"
    return result