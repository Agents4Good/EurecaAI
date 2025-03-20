import uuid, json, getpass, os, re
from typing import TypedDict, Annotated
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from ..prompts.prompts import AGENTE_ENTRADA_PROMPT
from ..tools.utils.most_similar import get_most_similar
from ..tools.curso.get_cursos import get_cursos
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

load_dotenv()

template = """
Você é um assistente inteligente que ajuda a reformular perguntas. 
Recebe uma pergunta de um usuário e deve identificar se há menção de múltiplos cursos. 
Se houver mais de um curso, você deve reformular a pergunta para deixar claro que cada um é tratado separadamente.
Reformule apenas adicionando a palavra 'curso' seguido do nome deste curso, faça isso para cada curso que você identificar.
Apenas reformule a pergunta e **retorne apenas a nova versão da pergunta, sem explicações adicionais ou comentários**.
IMPORTANTE: raciocine se na pergunta possui de fato algum nome de curso sendo perguntado, caso não tenha você NÃO DEVE MODIFICAR A PERGUNTA.

Pergunta: {question}
"""

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
        if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")

        prompt_template = PromptTemplate(template=template, input_variables=["question"])

        llm = HuggingFaceEndpoint(repo_id="maritaca-ai/sabia-7b", task="text-generation", temperature=0.1)
        messages = state["messages"]

        llm_chain = prompt_template | llm
        question = messages[0].content
        response = llm_chain.invoke({"question": question})
        response_text = re.sub(r"^Resposta:\s*", "", response.strip())
        human_msg_id = messages[-1].id
        return {'messages': [HumanMessage(content=response_text, id=human_msg_id)]}
    
    
    def processa_entrada_rag_node(self, state: AgentState):
        messages = state["messages"]
        pergunta = messages[-1].content

        mapper_curso = {"nome": "descricao", "codigo": "codigo_do_curso"}

        cursos = get_cursos()
        _, top_cursos = get_most_similar(lista_a_comparar=cursos, dado_comparado=pergunta, top_k=5, mapper=mapper_curso, limiar=0.5)

        top_cursos = [curso['nome'] for curso in top_cursos]

        print(top_cursos)

        AGENTE_ENTRADA_PROMPT2 = f"""
        Você é um assistente inteligente que reformula perguntas para garantir clareza ao tratar múltiplos cursos.  
        Recebe uma pergunta de um usuário e uma lista de cursos disponíveis.
        Se a pergunta mencionar múltiplos cursos, reformule-a para deixar claro que cada um deve ser tratado separadamente.
        Use a lista de cursos fornecida para garantir que a reformulação esteja correta e consistente com os cursos disponíveis.  
        Apenas reformule a pergunta e **retorne apenas a nova versão da pergunta, sem explicações adicionais ou comentários**.
        Modifique apenas o nome dos cursos na pergunta, não o objetivo dela.

        Lista de cursos disponíveis:
        {top_cursos}

        IMPORTANTE: raciocine se na pergunta possui de fato algum nome de curso sendo perguntado, caso não tenha você NÃO DEVE MODIFICAR A PERGUNTA.
        """

        #model_extra = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        model_extra = ChatOllama(model="llama3.1", temperature=0)
        if not messages or not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=AGENTE_ENTRADA_PROMPT2))
        response = model_extra.invoke(messages)
        human_msg_id = messages[-1].id
        return {'messages': [HumanMessage(content=response.content, id=human_msg_id)]}
    
    
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