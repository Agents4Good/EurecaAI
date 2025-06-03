from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from typing import TypedDict, Union, List
from IPython.display import Image, display
import time

llm = ChatOllama(model="llama3.2:3b", temperature=0)
class GraphState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, ToolMessage]]
    content: str


@tool
def get_periodo_atual() -> str:
    """
    _summary_
    Retorna o periodo atual.
    Se o período for 'X.1', então ele é o primeiro período do ano. Se o período for período 'X.2', então ele é segundo período do ano. 
    Um período tem uma data definida com data de início e data de término que não há um padrão para essas datas. 
    Então, você só deve responder com o período retornado pela resposta dessa ferramanta de get_periodo_atual.
    """
    
    return "Período atual: 2024.1"


def agente_periodos(state: GraphState) -> GraphState:
    tools = [get_periodo_atual]

    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(state["messages"]).tool_calls

    for call in response:
        choiced = { tool_i.name: tool_i for tool_i in tools }[call["name"]]
        print(f"\nAgentePeriodos: 🔧 ToolCalls \nToolName: {call['name']}\nParameters: ({call.get('args', '')}) \nID: {call['id']}")
        start = time.time()
        result = choiced.invoke(call)
        print(f"Time Execution: {round(time.time() - start, 9)} seconds\n")
        state["messages"].append(AIMessage(content=result.content, tool_call_id=call["id"]))

    return state


def agente_agregador(state: GraphState) -> GraphState:
    start = time.time()
    response = llm.invoke(state["messages"])
    print(f'\nAgenteAgregador: Message\nMessage: \n"""\n{response.content}\n"""\nTime Execution: {round(time.time() - start, 9)} seconds\n')
    state["messages"].append(response)
    return { "content": response.content, "messages": state["messages"] }


def agente_supervisor(state: GraphState) -> str:
    prompt = """
    Você é um agente supervisor que recebe uma pergunta e a encaminha para um agente especialista para responder a pergunta do usuário.
    agente_periodos sabe tudo sobre os períodos da universidade.

    Se você achar que a pergunta deve ser respondida pelo agente de periodos, responda apenas "agente_periodos";
    Se você achar que a pergunta foi respondida pelos agente de períodos, responda apenas "agente_agregador";
    """

    messages = state["messages"] + [HumanMessage(content=prompt)]
    start = time.time()
    response = llm.invoke(messages).content.strip().lower()
    print(f'\nAgenteSupervisor: Message\nMessage: \n"""\n{response}\n"""\nTime Execution: {round(time.time() - start, 9)} seconds\n')

    state["next_node"] = "agente_periodos" if "agente_periodos" in response else "agente_agregador"
    return state


builder = StateGraph(GraphState)
builder.add_node("agente_supervisor", agente_supervisor)
builder.add_node("agente_periodos", agente_periodos)
builder.add_node("agente_agregador", agente_agregador)

builder.set_entry_point("agente_supervisor")

builder.add_conditional_edges("agente_supervisor", lambda state: state["next_node"], {"agente_periodos": "agente_periodos", "agente_agregador": "agente_agregador"})
builder.add_edge("agente_periodos", "agente_supervisor")
builder.add_edge("agente_agregador", END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

entrada = {"messages": [HumanMessage(content="Qual é o período atual?")]}
saida = graph.invoke(entrada)

# print(saida)