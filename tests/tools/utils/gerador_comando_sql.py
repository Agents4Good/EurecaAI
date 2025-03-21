from langchain_ollama import ChatOllama

def gerador_comando_sql(prompt, pergunta):
    llm = ChatOllama(model="llama3.1", temperature=0)
    resposta = llm.invoke(prompt.format(pergunta))

    return resposta.content