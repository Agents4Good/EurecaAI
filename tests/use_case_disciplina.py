from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from .prompts.prompts import *
from .tools.disciplina.get_disciplina import get_disciplina
from .tools.disciplina.get_horarios_disciplinas import get_horarios_disciplinas
from .tools.disciplina.get_notas_turma_disciplina import get_notas_turma_disciplina
from .tools.disciplina.get_plano_aulas import get_plano_aulas
from .tools.disciplina.get_plano_curso_disciplina import get_plano_de_curso_disciplina
from .tools.disciplina.get_pre_requisitos_disciplina import get_pre_requisitos_disciplina
from .tools.disciplina.get_todas_disciplinas import get_todas_disciplinas
from .tools.disciplina.get_turmas_disciplina import get_turmas_disciplina

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

import uuid, json

from dotenv import load_dotenv


load_dotenv()

tools = [
    get_disciplina, 
    get_plano_aulas, 
    get_plano_de_curso_disciplina, 
    get_turmas_disciplina, 
    get_pre_requisitos_disciplina,
    get_horarios_disciplinas,
    get_notas_turma_disciplina,
    get_todas_disciplinas,
]

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

    #print("MSG ",messages)
    system_prompt = SystemMessage(
        content=ZERO_SHOT_PROMPT2
    )

    if not messages or not isinstance(messages[0], SystemMessage):
        messages.insert(0, system_prompt)
    
    response =  model_with_tools.invoke(messages)
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
    #{"messages": [("human", "Me dê informações da disciplina compiladores")]}, stream_mode="values"
    #{"messages": [("human", "quais são os horários de compiladores do curso de ciência da computação")]}, stream_mode="values"
    #{"messages": [("human", "quais as notas da disciplina de compiladores do curso de ciência da computação")]}, stream_mode="values"
    #{"messages": [("human", "qual o plano de aulas de teoria da computação do curso de ciência da computação da turma 1")]}, stream_mode="values"
    #{"messages": [("human", "qual o pré requisito de teoria da computação do curso de ciência da computação curriculo 2022")]}, stream_mode="values"
    {"messages": [("human", "quais são as turmas de teoria da computação de cieência da computação")]}, stream_mode="values"
):
    chunk["messages"][-1].pretty_print()
