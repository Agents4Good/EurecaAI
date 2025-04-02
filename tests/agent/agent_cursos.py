import getpass, os, re
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from .agent_tools import AgentTools, AgentState
from langgraph.graph import StateGraph, MessagesState, START, END

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

template = """
Você é um assistente inteligente que ajuda a reformular perguntas. 
Recebe uma pergunta de um usuário e deve identificar se há menção de múltiplos cursos. 
Se houver mais de um curso, você deve reformular a pergunta para deixar claro que cada um é tratado separadamente.
Reformule apenas adicionando a palavra 'curso' seguido do nome deste curso, faça isso para cada curso que você identificar.
Apenas reformule a pergunta e **retorne apenas a nova versão da pergunta, sem explicações adicionais ou comentários**.
IMPORTANTE: raciocine se na pergunta possui de fato algum nome de curso sendo perguntado, caso não tenha você NÃO DEVE MODIFICAR A PERGUNTA.

Pergunta: {question}
"""

class AgenteCursos(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)

    def processa_entrada_node(self, state: AgentState):
        if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")

        prompt_template = PromptTemplate(template=template, input_variables=["question"])

        llm = HuggingFaceEndpoint(repo_id="maritaca-ai/sabia-7b", task="text-generation", temperature=0.1)
        llm_chain = prompt_template | llm

        messages = state["messages"]
        question = messages[0].content
        print("PERGUNTA ORIGINAL: ", question)
        response = llm_chain.invoke({"question": question})
        print("PERGUNTA REFEITA: ", response)
        response_text = re.sub(r"^Resposta:\s*", "", response.strip())
        human_msg_id = messages[-1].id
        return {'messages': [HumanMessage(content=response_text, id=human_msg_id)]}

    def build(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("input", self.processa_entrada_node)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_node("exit", self.exit_node)
        workflow.add_edge(START, "input")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", "exit"])
        workflow.add_edge("input", "agent")
        workflow.add_edge("tools", "agent")
        workflow.add_edge("exit", END)
        return workflow.compile()
    
    def run(self, question: str):
        thread = {"configurable": {"thread_id": "1"}}
        '''output_file = "grafo.png"
        graph_image = self.app.get_graph().draw_mermaid_png()

        with open(output_file, "wb") as f:
            f.write(graph_image)'''
        
        for message_chunk, metadata in self.app.stream({"messages": [HumanMessage(content=question)]}, thread, stream_mode="messages"):
            if message_chunk.content:
                print(message_chunk.content, end="", flush=True)