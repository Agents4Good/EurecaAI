from langchain.schema import AIMessage, HumanMessage
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

def format_agent_responses(messages: list) -> tuple[str, str]:
    """
    Extrai a query e organiza as respostas por agente, em blocos separados apenas se houver múltiplas mensagens do mesmo agente.
    A ordem original das mensagens é preservada.
    """
    
    '''query = next((msg.content for msg in messages if isinstance(msg, HumanMessage)), "")
    
    # Agrupa respostas por agente
    agent_responses = defaultdict(list)
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.name:
            content = msg.content.strip()
            if content:
                agent_responses[msg.name].append(msg.content.strip())
    
    response_lines = []
    for agent, responses in agent_responses.items():
        # Caso haja muitas respostas do mesmo agente, junta tudo por blocos
        full_response = "\n\n---\n\n".join(responses)
        response_lines.append(f"'{agent}' respondeu:\n{full_response}")
    
    formatted_responses = "\n\n\n".join(response_lines)'''
    query = next((msg.content for msg in messages if isinstance(msg, HumanMessage)), "").strip()

    response_blocks = []
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.name:
            content = msg.content.strip()
            if content:
                response_blocks.append(f"'{msg.name}' respondeu:\n{content}")

    formatted_responses = "\n\n---\n\n".join(response_blocks)
    
    return query.strip(), formatted_responses.strip()