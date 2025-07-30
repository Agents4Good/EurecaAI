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


class AgenteTools:
    def __init__(
        self,
        LLM,
        model: str,
        tools: list,
        prompt: str,
        temperature: int = 0,
        max_tokens: int = 2000,
    ):
        self.model = LLM(
            model=model, temperature=temperature, max_tokens=max_tokens
        ).bind_tools(tools)
        self.tools = ToolNode(tools)
        self.prompt = prompt
        self.app = self.build()

    async def call_model(self, state: AgentState):
        messages = state["messages"]
        if self.prompt:
            messages = [SystemMessage(content=self.prompt)] + messages

        message = await self.model.ainvoke(messages)
        message = await self.extract_tool_calls(message)
    
        print("RESPOSTA DO AGENTE: ", message)
        return {'messages': [AIMessage(content=message.content, tool_calls=message.tool_calls)]}
    


    def build(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        # workflow.add_node("exit", self.exit_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", END])
        workflow.add_edge("tools", "agent")
        # workflow.add_edge("exit", END)
        return workflow.compile()
    
    async def should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    async def arun(self, question: str):
        # graph = self.build()
        # response = await graph.ainvoke({"messages": [HumanMessage(content=question)]})

        # return response
        thread = {"configurable": {"thread_id": "1"}}
        auxiliar = ""
        async for message_chunk in self.app.astream(
            {"messages": [HumanMessage(content=question)]},
            thread,
            stream_mode="values",
        ):
                message = message_chunk["messages"][-1]
                auxiliar = message
                message.pretty_print()

        return auxiliar.content


    async def extract_tool_calls(self, response):
        try:
            content_data = json.loads(response.content)
            if "tool_calls" in content_data:
                tool_calls = content_data["tool_calls"]

                for tool_call in tool_calls:
                    tool_call.setdefault("id", str(uuid.uuid4()))
                    tool_call.setdefault("type", "tool_call")
                
                response.tool_calls = tool_calls
                response.content = content_data.get("content", "")
        
        except json.JSONDecodeError:
            pattern = r"<function=([a-zA-Z_][a-zA-Z0-9_]*)>\s*(\{.*?\})(?:\s*;)?"
            matches = re.findall(pattern, response.content)

            tool_calls = []
            for func_name, args_json in matches:
                try:
                    args = json.loads(args_json)
                    tool_call = {
                        "name": func_name,
                        "args": args,
                        "id": str(uuid.uuid4()),
                        "type": "tool_call"
                    }
                    tool_calls.append(tool_call)
                except json.JSONDecodeError:
                    continue
            
            if tool_calls:
                response.tool_calls = tool_calls
                response.content = ""
                response.response_metadata["finish_reason"] = "tool_calls"
        return response

