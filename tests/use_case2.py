from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.schema import SystemMessage
from langchain_core.messages import HumanMessage

from .tools.curso_tools import *
from .prompts.prompts import *

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

import uuid, json

from dotenv import load_dotenv

load_dotenv()

tools = [
    get_cursos, 
    get_codigo_curso, 
    get_informacoes_curso, 
    get_estudantes
] # tools para testar aqui
tool_node = ToolNode(tools)

model_with_tools = ChatOllama(model="llama3.1", temperature=0).bind_tools(tools)
#model_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
#model_with_tools = ChatNVIDIA(model="meta/llama-3.3-70b-instruct").bind_tools(tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

def extract_tool_calls(response):
    try:
        content_data = json.loads(response.content)
        if "tool_calls" in content_data:
            tool_calls = content_data["tool_calls"]

            for tool_call in tool_calls:
                tool_call.setdefault("id", str(uuid.uuid4()))  # Gera um UUID único se não existir
                tool_call.setdefault("type", "tool_call")  # Define o tipo
            
            response.tool_calls = tool_calls
            response.content = content_data.get("content", "")
    except json.JSONDecodeError:
        pass
    return response

def call_model(state: MessagesState):
    messages = state["messages"]

    system_prompt = SystemMessage(
        content=ZERO_SHOT_PROMPT2
    )

    if not messages or not isinstance(messages[0], SystemMessage):
        messages.insert(0, system_prompt)
    
    response = model_with_tools.invoke(messages)
    response = extract_tool_calls(response)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()

'''from IPython.display import Image

file = "grafo.png"
img = app.get_graph().draw_mermaid_png()
with open(file, "wb") as f:
    f.write(img)'''

for chunk in app.stream(
    #{"messages": [("human", "Qual a quantia de estudantes pardos em ciência da computação?")]}, stream_mode="values"
    #{"messages": [("human", "Qual o código do curso de história diurno?")]}, stream_mode="values"
    #{"messages": [("human", "qual o nome do setor e o seu código para o curso de historia diurno")]}, stream_mode="values"
    #{"messages": [("human", "Qual o nome do setor e o seu código para o curso de historia diurno, ciência da computação e engenharia civil?")]}, stream_mode="values"
    {"messages": [("human", "Qual o código do curso de economicas")]}, stream_mode="values"
):
    chunk["messages"][-1].pretty_print()