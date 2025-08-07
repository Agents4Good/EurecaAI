
import json
import re
import traceback
import uuid
from typing import TypedDict, Annotated, Any

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_community.chat_models import ChatDeepInfra
from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable



def reduce_messages(
    left: list[AnyMessage], right: list[AnyMessage]
) -> list[AnyMessage]:
    for message in right:
        if not message.id:
            message.id = str(uuid.uuid4())
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            merged.append(message)
    return merged


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]


class AgenteToolsSemSuporte:
    def __init__(
        self,
        LLM,
        model: str,
        tools: list,
        prompt: str,
        temperature: int = 0,
        max_tokens: int = 2000,
        session=None,  # sessão MCP para executar as tools
    ):
        self.model = LLM(model=model, temperature=temperature, max_tokens=max_tokens)
        
        self.manual_tool_binding = None
        self.tools = tools
        self.prompt = prompt
        self.session = session
        self.app = self.build()


    async def call_model(self, state: AgentState):
        messages = state["messages"]
        if self.prompt:
            messages = [SystemMessage(content=self.prompt)] + messages

        message = await self.model.ainvoke(messages)
        matches = re.findall(r"use_tool\((\w+),\s*(\{.*?\})\)", message.content)

        tool_calls = []
        for name, raw_args in matches:
            try:
                raw_args_json = raw_args.replace("'", '"')
                args = json.loads(raw_args_json)
                tool_calls.append({"id": str(uuid.uuid4()), "name": name, "args": args})

            except json.JSONDecodeError:
                print(f"[!] Erro ao decodificar JSON dos argumentos: {raw_args}")

        #state["manual_tool_calls"] = tool_calls
        return {'messages': [AIMessage(content=message.content, call_server=tool_calls)]}
    

    async def agreggator(self, state: AgentState):
        last_message = state["messages"][-1]
        raw_tool_response = last_message.content

        messages = state["messages"]
        original_question = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                original_question = msg.content
                break

        if original_question is None:
            original_question = "Pergunta original não encontrada."

        prompt = (
            f"Você recebeu a seguinte pergunta:\n{original_question}\n\n"
            f"E esta foi a resposta bruta da ferramenta:\n{raw_tool_response}\n\n"
            f"Formule uma resposta clara e amigável para o usuário com base nisso."
        )

        prompt_messages = [
            SystemMessage(content="Você é um assistente que reformula e explica respostas técnicas."),
            HumanMessage(content=prompt),
        ]
        refined_message = await self.model.ainvoke(prompt_messages)
        return {'messages': [AIMessage(content=refined_message.content)]}

    def build(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("call_server", self.call_server)
        workflow.add_node("agreggator", self.agreggator)  
    
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["call_server", "agreggator", END])
        workflow.add_edge("call_server", "agreggator")
        workflow.add_edge("agreggator", "agent")
        # workflow.add_conditional_edges(
        #     "agreggator",
        #     self.should_continue,  # função que decide se vai para END ou continua
        #     ["agent", END]
        # )

        #workflow.add_edge("call_server", "agent")
        return workflow.compile()
    

    async def call_server(self, state: AgentState):
        last_message = state["messages"][-1]
        response = []

        for tool_call in last_message.call_server:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"[EXECUTE TOOL] Executando tool '{tool_name}' com args: {tool_args}")
            tool_result = await self.session.call_tool(tool_name, arguments=tool_args)
            #print("Resultado da tool:", tool_result)
            for content_item in tool_result.content:
                response.append(content_item.text)

        return {'messages': [AIMessage(content=",".join(response))]}

    async def should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.call_server:
            return "call_server"
        return END

    async def arun(self, question: str):
        thread = {"configurable": {"thread_id": "1"}}
        auxiliar = ""
        async for message_chunk in self.app.astream(
            {"messages": [HumanMessage(content=question)]},
            thread,
            stream_mode="values",
        ):
                message = message_chunk["messages"][-1]
                if message.content and message.content.strip() != "":
                    auxiliar = message
                message.pretty_print()

        return auxiliar.content
    
