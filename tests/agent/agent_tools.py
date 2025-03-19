import uuid, json
from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from ..prompts.prompts import AGENTE_ENTRADA_PROMPT
from ..tools.utils.most_similar import get_most_similar
from ..tools.curso.get_cursos import get_lista_cursos
from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama

def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid.uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]


class AgentTools:
    def __init__(self, LLM, model: str, tools: list, prompt: str, temperatura: int = 0):
        self.model = LLM(model=model, temperature=temperatura).bind_tools(tools)
        self.tools = ToolNode(tools)
        self.prompt = prompt
        self.app = self.build()
    
    
    def call_model(self, state: AgentState):
        messages = state["messages"]
        if self.prompt:
            messages = [SystemMessage(content=self.prompt)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}
    

    def processa_entrada_node(self, state: AgentState):
        messages = state["messages"]
        model_extra = ChatOllama(model="gemma3", temperature=0)
        messages = [SystemMessage(content=AGENTE_ENTRADA_PROMPT)] + messages
        response = model_extra.invoke(messages)
        human_msg_id = messages[-1].id
        return {'messages': [HumanMessage(content=response.content, id=human_msg_id)]}
    
    
    def processa_entrada_rag_node(self, state: AgentState):
        messages = state["messages"]
        pergunta = messages[-1].content

        mapper_curso = {"nome": "descricao", "codigo": "codigo_do_curso"}

        cursos = get_lista_cursos()
        _, top_cursos = get_most_similar(lista_a_comparar=cursos, dado_comparado=pergunta, top_k=5, mapper=mapper_curso, limiar=0.5)

        top_cursos = [curso['nome'] for curso in top_cursos]

        AGENTE_ENTRADA_PROMPT2 = f"""
        Você é um assistente inteligente que reformula perguntas para garantir clareza ao tratar múltiplos cursos.  
        Recebe uma pergunta de um usuário e uma lista de cursos disponíveis.  
        Se a pergunta mencionar múltiplos cursos, reformule-a para deixar claro que cada um deve ser tratado separadamente.  
        Use a lista de cursos fornecida para garantir que a reformulação esteja correta e consistente com os cursos disponíveis.  
        Apenas reformule a pergunta e **retorne apenas a nova versão da pergunta, sem explicações adicionais ou comentários**.
        Modifique apenas o nome dos cursos na pergunta, não o objetivo dela.

        Lista de cursos disponíveis:
        {top_cursos}
        """

        model_extra = ChatOllama(model="gemma3", temperature=0)
        if not messages or not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=AGENTE_ENTRADA_PROMPT2))
        resposta = model_extra.invoke(messages)
        human_msg_id = messages[-1].id
        return {"messages": [HumanMessage(content=resposta.content, id=human_msg_id)]}
    
    
    def build(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("processa_entrada", self.processa_entrada_node)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_edge(START, "processa_entrada")
        workflow.add_edge("processa_entrada", "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", END])
        workflow.add_edge("tools", "agent")
        return workflow.compile()

        
    def should_continue(self, state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END
    
    
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
            pass
        return response
    
    
    def run(self, question: str):
        thread = {"configurable": {"thread_id": "1"}}
        '''for chunk in self.app.stream({"messages": [("human", question)]}, thread, stream_mode="values"):
            chunk["messages"][-1].pretty_print()'''
        for chunk in self.app.stream({"messages": [HumanMessage(content=question)]}, thread, stream_mode="values"):
            chunk["messages"][-1].pretty_print()