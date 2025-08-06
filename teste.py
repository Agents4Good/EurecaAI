import asyncio
from typing import Annotated, TypedDict
import uuid
from langgraph.graph import StateGraph

from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_mcp_adapters.tools import load_mcp_tools
from  client.mcp_client import MCPClient  # Sua implementação MCP client
from langchain_community.chat_models import ChatDeepInfra

from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)



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

class AgenteLangGraph:
    def __init__(self, tools, model_name):
        self.tools = tools
        self.model = ChatDeepInfra(model=model_name, temperature=0)
        self.tool_node = ToolNode(tools)  # Não executa localmente, só roteia pro MCP server

        self.workflow = StateGraph(AgentState)
        self.workflow.add_node("agent", self.call_model)
        self.workflow.add_node("tools", self.tool_node)
        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges("agent", self.should_continue, ["tools", END])
        self.workflow.add_edge("tools", "agent")

        self.prompt = "Você é um assistente universitário e pode usar ferramentas para responder perguntas."
     
        self.graph = self.workflow.compile()

    
    async def should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]


        if last_message.tool_calls:
            return "tools"
        return END
    
    async def call_model(self, state: AgentState):
        messages = state["messages"]
        if self.prompt:
            messages = [SystemMessage(content=self.prompt)] + messages
        response = await self.model.ainvoke(messages)
        # O modelo não executa tools, apenas retorna tool_call na mensagem
        return {"messages": messages + [response]}

    async def run(self, question: str):
        state = {"messages": [HumanMessage(content=question)]}
        state = await self.graph.ainvoke(state)
        print("DEBUG: mensagens finais:", state["messages"])
        return state["messages"][-1].content

async def main():
    mcp_client = MCPClient()
    await mcp_client.connect_to_server("/home/beatriz/agents4good/EurecaAIMCP/eureca/main.py")

    try:
        tools = await load_mcp_tools(mcp_client.session)
        agent = AgenteLangGraph(tools, "meta-llama/Llama-Guard-3-8B")

        print("🤖 Pergunte algo (quit para sair):")
        while True:
            question = input("Você: ")
            if question.lower() == "quit":
                break
            answer = await agent.run(question)
            print("Resposta:", answer)
    finally:
        try:
            await mcp_client.session_cm.__aexit__(None, None, None)
        except GeneratorExit:
            pass

import asyncio

async def safe_main():
    try:
        await main()
    except GeneratorExit:
        pass

if __name__ == "__main__":
    asyncio.run(safe_main())

