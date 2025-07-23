import json
from langchain_core.language_models import BaseChatModel

def generate_chat_title(text: str, llm: BaseChatModel):
    """
    """

    resposta = llm.invoke(
            f"""
            "Gere um título de até 3 palavras para o texto a seguir:
            {text}
            
            *IMPORTANTE*:
            - Você sempre deve gerar um título, não faça nada além disso.
            - Sempre gere no seguinte formato: {{"titulo": "titulo_gerado"}}
            """
        )
    print("RESUMO PARA O TÍTULO: ", resposta)
    resumo = resposta.content if hasattr(resposta, "content") else str(resposta)
    resumo = resumo.replace("'", '"')
    return json.loads(resumo)