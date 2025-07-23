from langchain.schema import AIMessage, HumanMessage, BaseMessage

from typing import Literal
from pydantic import BaseModel

# AGENTES ESPECIALIZADOS DO SISTEMA
MEMBERS = [
    "Agente_Curso",
    "Agente_Disciplina",
    "Agente_Estudante",
    "Agente_Setor"
]

# FORMATO DE RETORNO PARA A RESPOSTA DO SUPERVISOR
class RouteResponse(BaseModel):
    next: Literal[
        "Agente_Curso",
        "Agente_Disciplina",
        "Agente_Estudante",
        "Agente_Setor",
        "FINISH"
    ]


#====ABAIXO SÃO FUNÇÕES AUXILIARES====#

def extract_next_agent(response: BaseMessage) -> str:
    """
    Extrai o campo 'next' de uma resposta do supervisor no formato JSON.
    """

    try:
        parsed = RouteResponse.model_validate_json(response.content)
        return parsed.next
    except Exception as e:
        raise ValueError(f"Erro ao extrair 'next' da resposta: {response.content}") from e

def format_agent_responses(messages: list[HumanMessage | AIMessage]) -> tuple[str, str]:
    """
    Formata as respostas dos agentes especializados para a interação atual.
    """

    # Pega a posição da última HumanMessage
    last_user_index = next(
        (i for i in reversed(range(len(messages))) if isinstance(messages[i], HumanMessage)),
        None
    )

    if last_user_index is None:
        return "", ""

    query = messages[last_user_index].content.strip()

    response_blocks = []
    for msg in messages[last_user_index + 1:]:
        if isinstance(msg, AIMessage) and msg.name:
            content = msg.content.strip()
            if content:
                response_blocks.append(f"'{msg.name}' respondeu:\n{msg.content}")

    formatted_responses = "\n\n---\n\n".join(response_blocks)

    return query, formatted_responses.strip()

def format_context(messages: list[HumanMessage | AIMessage], last_n_pairs: int = 1) -> str:
    """
    Formata os últimos N pares HumanMessage -> Agente_Agregador.
    """

    if len(messages) == 1 and isinstance(messages[0], HumanMessage):
        return ""
    
    if isinstance(messages[-1], HumanMessage):
        messages = messages[:-1]
    
    filtered = [
        msg for msg in messages
        if isinstance(msg, HumanMessage) or (isinstance(msg, AIMessage) and msg.name == "Agente_Agregador")
    ]

    # Agrupamento de pares (Human -> Agente_Agregador)
    recent_msgs = filtered[-(last_n_pairs * 2):]
    pairs = [
        (recent_msgs[i], recent_msgs[i + 1])
        for i in range(0, len(recent_msgs), 2)
    ]

    return "\n\n---\n\n".join(
        f"Usuário perguntou:\n{human.content.strip()}\n\nResposta encontrada:\n{agent.content.strip()}"
        for human, agent in pairs
    )

def format_context_to_summarize(messages: list[HumanMessage | AIMessage]) -> str:
    """
    Formata todos os pares Human -> Agente_Agregador, exceto o último, para gerar um resumo.
    """
    filtered = [
        msg for msg in messages
        if isinstance(msg, HumanMessage) or (isinstance(msg, AIMessage) and msg.name == "Agente_Agregador")
    ]

    pairs = []
    i = 0
    while i < len(filtered) - 1:
        if isinstance(filtered[i], HumanMessage) and isinstance(filtered[i+1], AIMessage):
            pairs.append((filtered[i], filtered[i+1]))
            i += 2
        else:
            i += 1

    if len(pairs) <= 1:
        return ""

    return "\n\n---\n\n".join(
        f"Usuário perguntou:\n{h.content.strip()}\n\nResposta encontrada:\n{a.content.strip()}"
        for h, a in pairs[:-1]
    )