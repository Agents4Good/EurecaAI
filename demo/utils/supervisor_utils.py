import json, re

from langchain.schema import AIMessage, HumanMessage, BaseMessage
from langchain.output_parsers import PydanticOutputParser

from typing import Literal
from pydantic import BaseModel
from collections import defaultdict


# AGENTES ESPECIALIZADOS DO SISTEMA
MEMBERS = [
    "Agente_Curso",
    "Agente_Disciplina"
]

# FORMATO DE RETORNO PARA A RESPOSTA DO SUPERVISOR
class RouteResponse(BaseModel):
    next: Literal[
        "Agente_Curso",
        "Agente_Disciplina",
        "FINISH"
    ]

def get_supervisor_output_parser() -> tuple:
    """
    Cria e retorna um output parser baseado em Pydantic para validar e estruturar as respostas do supervisor.
    """

    output_parser = PydanticOutputParser(pydantic_object=RouteResponse)
    format_instructions = output_parser.get_format_instructions()
    return output_parser, format_instructions

def extract_next_agent(response: BaseMessage) -> str:
    """
    Extrai o campo 'next' de uma resposta do supervisor no formato JSON.
    """

    try:
        parsed = RouteResponse.model_validate_json(response.content)
        return parsed.next
    except Exception as e:
        raise ValueError(f"Erro ao extrair 'next' da resposta: {response.content}") from e

def format_agent_responses(messages: list) -> tuple[str, str]:
    """
    Extrai a query e organiza as respostas por agente, em blocos separados apenas se houver múltiplas mensagens do mesmo agente.
    A ordem original das mensagens é preservada.
    """

    query = next((msg.content for msg in messages if isinstance(msg, HumanMessage)), "").strip()

    response_blocks = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.name:
            content = msg.content.strip()
            if content:
                response_blocks.append(f"'{msg.name}' respondeu:\n{content}")

    formatted_responses = "\n\n---\n\n".join(response_blocks)
    
    return query.strip(), formatted_responses.strip()