import uuid, json, re
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.schema import SystemMessage
from ..prompts.prompts import AGENTE_ENTRADA_PROMPT
from ..tools.utils.most_similar import get_most_similar
from ..tools.curso.get_cursos import get_cursos
from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama

class AgentTools:
    def __init__(self, LLM, model: str, tools: list, prompt: str, temperatura: int = 0):
        self.model = LLM(model=model, temperature=temperatura).bind_tools(tools)
        self.tools = ToolNode(tools)
        self.prompt = prompt
        self.app = self.build()
    
    
    def call_model(self, state: MessagesState):
        messages = state["messages"]
        if not messages or not isinstance(messages[-1], SystemMessage):
            messages.insert(0, SystemMessage(content=self.prompt))
        return {"messages": [self.extract_tool_calls(self.model.invoke(messages))]}
    

    def processa_entrada_node(self, state: MessagesState):
        messages = state["messages"]
        model_extra = ChatOllama(model="gemma3", temperature=0)
        if not messages or not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=AGENTE_ENTRADA_PROMPT))
        resposta = model_extra.invoke(messages)
        return {"messages": [resposta.content]}
    
    def processa_entrada_rag_node(self, state: MessagesState):
        messages = state["messages"]
        pergunta = messages[-1].content

        mapper_curso = {"nome": "descricao", "codigo": "codigo_do_curso"}

        cursos = get_cursos()
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

        #model_extra = ChatOllama(model="llama3.1", temperature=0.2)
        model_extra = ChatOllama(model="gemma3", temperature=0)
        if not messages or not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=AGENTE_ENTRADA_PROMPT2))
        print(messages)
        resposta = model_extra.invoke(messages)
        print(resposta)
        return {"messages": [resposta.content]}
    
    
    def build(self):
        workflow = StateGraph(MessagesState)
        workflow.add_node("processa_entrada", self.processa_entrada_node)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_edge(START, "processa_entrada")
        workflow.add_edge("processa_entrada", "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", END])
        workflow.add_edge("tools", "agent")
        return workflow.compile()

        
    def should_continue(self, state: MessagesState):
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
        '''from IPython.display import Image

        file = "grafo.png"
        img = self.app.get_graph().draw_mermaid_png()
        with open(file, "wb") as f:
            f.write(img)'''
        
        for chunk in self.app.stream({"messages": [("human", question)]}, stream_mode="values"):
            chunk["messages"][-1].pretty_print()