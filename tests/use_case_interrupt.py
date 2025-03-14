from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import interrupt, Command
from langchain.schema import SystemMessage
from langchain_core.messages import HumanMessage, ToolMessage

from .tools.curso.get_curso import get_curso
from .tools.curso.get_cursos import get_cursos
from .tools.curso.get_estudantes_curso import get_estudantes_curso
from .tools.curso.get_todos_curriculos_curso import get_curriculos
from .tools.curso.get_curriculo_mais_recente_curso import get_curriculo_mais_recente_curso
from .prompts.prompts import *

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from pydantic import BaseModel

import uuid, json, asyncio

from dotenv import load_dotenv

load_dotenv()

tools = [
    get_curso,
    get_cursos,
    get_estudantes_curso,
    get_curriculos,
    get_curriculo_mais_recente_curso,
]
tool_node = ToolNode(tools)

class AskHuman(BaseModel):
    """
    Perguntar ao usuário.
    """

model_with_tools = ChatOllama(model="llama3.1", temperature=0).bind_tools(tools + [AskHuman])
#model_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools + [AskHuman])
#model_with_tools = ChatNVIDIA(model="meta/llama-3.3-70b-instruct").bind_tools(tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        if last_message.tool_calls[0]["name"] == "AskHuman":
            return "ask_human"
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

def ask_human_node(state: MessagesState):
    messages = state["messages"]
    prev_msg = messages[-2]
    tool_call_id = messages[-1].tool_calls[0]["id"]
    if isinstance(prev_msg, ToolMessage):
        try:
            tool_msg_data = json.loads((prev_msg.content).replace("'", '"'))
            if 'AskHuman' in tool_msg_data and 'choice' in tool_msg_data:
                choices = tool_msg_data['choice']
                human_response = interrupt({
                    "message": f"Por favor, forneça um nome de curso válido. Os cursos mais prováveis encontrados são: {choices}"
                })
                tool_message = [{"tool_call_id": tool_call_id, "type": "tool", "content": human_response}]
                return {"messages": tool_message}
            return Command(goto="agent", update={"messages": [{"tool_call_id": tool_call_id, "type": "tool", "content": "Não foi possível responder essa pergunta."}]})
        except json.JSONDecodeError:
            return Command(goto="agent", update={"messages": [{"tool_call_id": tool_call_id, "type": "tool", "content": "Não foi possível responder essa pergunta."}]})
    return Command(goto="agent", update={"messages": [{"tool_call_id": tool_call_id, "type": "tool", "content": "Não foi possível responder essa pergunta."}]})

def call_model(state: MessagesState):
    messages = state["messages"]

    system_prompt = SystemMessage(
        content=ZERO_SHOT_PROMPT
    )

    if not messages or not isinstance(messages[0], SystemMessage):
        messages.insert(0, system_prompt)
    
    response = model_with_tools.invoke(messages)
    response = extract_tool_calls(response)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_node("ask_human", ask_human_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", "ask_human", END])
workflow.add_edge("tools", "agent")
workflow.add_edge("ask_human", "agent")


from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

app = workflow.compile(checkpointer=memory)

'''from IPython.display import Image

file = "grafo_human.png"
img = app.get_graph().draw_mermaid_png()
with open(file, "wb") as f:
    f.write(img)'''

async def run(app, config: dict):
    async for chunk in app.astream(
        {"messages": [("human", "me traga mais detalhes de economia, qual o nome do setor?")]}, config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
    
    state = await app.aget_state(config)
    if state.tasks and state.tasks[0].name == "ask_human":
        print(state.tasks[0].interrupts[0].value)
        resposta = input()
        async for chunk in app.astream(Command(resume=resposta), config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()

async def main():
    config = {"configurable": {"thread_id": "1"}}
    await run(app, config)

if __name__ == '__main__':
    asyncio.run(main())