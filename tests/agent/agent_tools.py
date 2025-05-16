import uuid, json, getpass, os, re
from typing import TypedDict, Annotated, Any
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from ..prompts.prompts import AGENTE_ENTRADA_PROMPT
from langchain_community.chat_models import ChatDeepInfra

from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama
#from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
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
    user_token: dict[str, Any]


class AgentTools:
    def __init__(self, LLM, model: str, tools: list, prompt: str, temperatura: int = 0, max_tokens: int = 2000):
        self.model = LLM(model=model, temperature=temperatura, max_tokens=max_tokens).bind_tools(tools)
        self.tools = ToolNode(tools)
        self.prompt = prompt
        self.app = self.build()
    

    def token_node(self, state: AgentState):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMjAyMTAxNjQiLCJjb2RlIjoiMTQxMDIxMDAiLCJpc3MiOiIiLCJuYW1lIjoiTUFUSEVVUyBIRU5TTEVZIERFIEZJR1VFSVJFRE8gRSBTSUxWQSIsImV4cCI6IjE3NDY4ODcwNzk0MjgiLCJ0eXBlIjoiQWx1bm8iLCJlbWFpbCI6Im1hdGhldXMuZmlndWVpcmVkby5zaWx2YUBjY2MudWZjZy5lZHUuYnIifQ==.ZSSSWf7hsRmPu4hmBiCXkase1gKHIIZMiXgdNbgyQYpDtY9OEJHXjsH5EYITIZqgkPSsZ6G2FVvCW1cyNUe-rYtHj6U52hMR8yBxxCYirozgWSzimG1IuPMYYT2XQ1ruWLofjLmZg5ye_poQ7PWATSs1ZQt9CuGgXSisMtJeFUejraYO7VSGl79pqsALaw6AYU7lM-wMag6CSKg0ZaASmsdDhLEP0q7n2WqetjCFKj282Z6DTAXys_mkdY3SthI4YjKHlyzYZsYJzjMM_B0eWOD89Y7QamtrzsJit6hgo7bWXaVSb6Mfox3DjVN-soSMJ9hR9NDLYrWnFgN89qQGWw=="
        return Command(
            update={"user_token": token}
        )
    
    def insert_token(self, state: AgentState, tool_calls: list):
        user_token = state.get("user_token", {})
        if not user_token:
            return tool_calls
        
        for tool_call in tool_calls:
            args = tool_call.get("args", {})
            if "token" in args:
                args["token"] = user_token  # sobrescreve o valor com o token correto
                tool_call["args"] = args  # atualiza de volta na tool_call
        
        return tool_calls
    
    def call_model(self, state: AgentState):
        #print("TOKEN DO USUÁRIO: ", state["user_token"])
        messages = state["messages"]
        if self.prompt:
            messages = [SystemMessage(content=self.prompt)] + messages
        message = self.model.invoke(messages)
        message = self.extract_tool_calls(message)
        # if message.tool_calls:
        #     message.tool_calls = self.insert_token(state, message.tool_calls)
        #     print("\nFEZ TOOL_CALL!!!!!!!!!\n")
        #     print(message.tool_calls)
        # else:
        #     print("\nNÃO FEZ TOOL_CALL!!!!!!!!")
        print("RESPOSTA DO AGENTE: ", message)
        return {'messages': [AIMessage(content=message.content, tool_calls=message.tool_calls)]}
    
    
    def exit_node(self, state: AgentState):
        messages = state["messages"]
        
        question = messages[0].content if isinstance(messages[0], HumanMessage) else ""
        '''tool_responses = [
            str(msg.content) if isinstance(msg.content, list) else msg.content
            for msg in messages if isinstance(msg, ToolMessage) and msg.content
        ]'''
        tool_responses = [
            msg.content for msg in messages
            if isinstance(msg, ToolMessage) and msg.content not in ("", "[]", "[[]]") and msg.content != []
        ]
        #ai_response = next((msg.content for msg in messages if isinstance(msg, AIMessage) and msg.content), "")

        #local_model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)
        local_model = ChatOllama(model="qwen3:4b", temperature=0)
        auxiliar = '\n'.join(tool_responses) if tool_responses else "Nenhuma resposta encontrada."

        response = local_model.invoke(
            f"""
            Pergunta do usuário:
            {question}
            
            Respostas encontradas pelas ferramentas:
            {auxiliar}
            
            Baseado nas respostas das ferramentas, faça uma interpretação para verificar se elas respondem de forma geral à pergunta do usuário. Elas não precisam responder de forma exata, só que façam sentido com a pergunta no geral.
            - Se não, informe que não foi possível encontrar uma resposta satisfatória.
            - Se sim, o que você deve fazer então é gerar uma resposta final clara e coesa com base nas respostas das ferramentas, você deve responder apenas com essa resposta final gerada e mais nada além disso. E não mencione que foi baseado nas ferramentas e sim nas informações que você tem à disposição.
            - Importante: se tiver nenhuma resposta encontrada pelas ferramentas, náo tente responder a pergunta do usuário, apenas informe que não foi possível encontrar uma resposta satisfatória.

            Sempre responda seguindo o modelo abaixo para a sua resposta final.

            <RESPOSTA>resposta final</RESPOSTA>
            """
        )
        return {'messages': [AIMessage(content=response.content)]}
    
    
    def build(self):
        workflow = StateGraph(AgentState)
        #workflow.add_node("token", self.token_node)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_node("exit", self.exit_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", "exit"])
        #workflow.add_edge("token", "agent")
        workflow.add_edge("tools", "agent")
        workflow.add_edge("exit", END)
        return workflow.compile()

        
    def should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return 'exit'
    
    
    def extract_tool_calls(self, response):
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
    
    
    def run(self, question: str):
        thread = {"configurable": {"thread_id": "1"}}
        for message_chunk in self.app.stream({"messages": [HumanMessage(content=question)]}, thread, stream_mode="values"):
            message_chunk["messages"][-1].pretty_print()