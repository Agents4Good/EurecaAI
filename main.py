from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from typing import TypedDict, Union, List

llm = ChatOllama(model="llama3.2:3b", temperature=0)
class GraphState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, ToolMessage]]
    content: str


@tool
def get_periodo_atual() -> str:
    """
    _summary_
    Retorna o periodo atual
    """
    
    return "2024.1"


def agente_periodos(state: GraphState) -> GraphState:
    tools = [get_periodo_atual]

    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(state["messages"]).tool_calls

    for call in response:
        choiced = { tool_i.name: tool_i for tool_i in tools }[call["name"]]
        result = choiced.invoke(call)
        state["messages"].append(ToolMessage(content=result.content, tool_call_id=call["id"]))

    return state


def agente_agregador(state: GraphState) -> GraphState:
    resposta = llm.invoke(state["messages"])
    state["messages"].append(resposta)
    return { "content": resposta.content, "messages": state["messages"] }


def agente_supervisor(state: GraphState) -> str:
    return state


def decidir_proximo_agente(state: GraphState) -> str:
    prompt = """
    Você é um agente supervisor que recebe uma pergunta e a encaminha para um agente especialista para responder a pergunta do usuário.

    Se você achar que a pergunta deve ser respondida pelo agente de periodos, responda apenas "agente_periodos";
    Se você achar que a pergunta foi respondida pelos agente de períodos, responda apenas "agente_agregador";
    """

    messages = state["messages"] + [HumanMessage(content=prompt)]
    response = llm.invoke(messages).content.strip().lower()

    if "agente_periodos" in response:
        return "agente_periodos"
    return "agente_agregador"



builder = StateGraph(GraphState)
builder.add_node("agente_supervisor", agente_supervisor)
builder.add_node("agente_periodos", agente_periodos)
builder.add_node("agente_agregador", agente_agregador)

builder.set_entry_point("agente_supervisor")

builder.add_conditional_edges("agente_supervisor", decidir_proximo_agente, {"agente_periodos": "agente_periodos", "agente_agregador": "agente_agregador"})
builder.add_edge("agente_periodos", "agente_supervisor")
builder.add_edge("agente_agregador", END)

graph = builder.compile()

entrada = {"messages": [HumanMessage(content="Qual é o período atual?")]}
saida = graph.invoke(entrada)

print(saida)
