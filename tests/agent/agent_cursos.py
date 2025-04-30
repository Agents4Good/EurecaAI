import getpass, os, re
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from .agent_tools import AgentTools, AgentState
from langgraph.graph import StateGraph, MessagesState, START, END

from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatDeepInfra
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

# template = """
# Você é um assistente inteligente que reformula perguntas de forma criteriosa. 
# Seu objetivo é identificar se a pergunta menciona dois ou mais cursos universitários pelo NOME. 
# Se e somente se houver múltiplos cursos claramente mencionados pelo nome (como 'Direito', 'Engenharia Civil', 'Medicina', etc), você deve reformular a pergunta para deixar explícito que cada curso está sendo considerado separadamente.

# Regras IMPORTANTES:
# - NÃO adicione ou invente nomes de cursos que não estão mencionados explicitamente.
# - Se a pergunta falar apenas de uma instituição (como 'Quantos cursos tem a UFCG?'), NÃO modifique a pergunta.
# - Se houver nomes genéricos como 'cursos', mas sem especificar quais, NÃO modifique a pergunta.
# - Reformule a pergunta apenas se houver mais de um curso com nome claro.

# Agora, reformule a seguinte pergunta obedecendo estritamente as regras mencionadas:

# Pergunta: {question}
# """

# template = """
# Você é um assistente inteligente que reformula perguntas de forma criteriosa. 
# Seu objetivo é identificar se a pergunta menciona dois ou mais cursos universitários pelo NOME. 
# Se e somente se houver múltiplos cursos claramente mencionados pelo nome, você deve reformular a pergunta para deixar explícito que cada curso está sendo considerado separadamente.

# Regras IMPORTANTES:
# - NÃO adicione ou invente nomes de cursos que não estão mencionados explicitamente.
# - Se a pergunta falar apenas de uma instituição (como 'Quantos cursos tem a UFCG?'), NÃO modifique a pergunta.
# - Se houver nomes genéricos como 'cursos', mas sem especificar quais, NÃO modifique a pergunta.
# - Reformule a pergunta apenas se houver mais de um curso com nome claro.
# - Mesmo se não houver necessidade de reformulação, retorne a pergunta no formato correto.

# Agora, reformule a seguinte pergunta obedecendo estritamente as regras mencionadas:

# Pergunta: {question}

# Mesmo que não haja necessidade de reformular a pergunta, mesmo assim repita a pergunta no seguinte formato (seja a pergunta reformulada ou não):

# Pergunta reformulada: `COLOQUE A PERGUNTA AQUI`
# """

template = """
Você é um assistente responsável por reformular perguntas de maneira criteriosa e objetiva.

Seu objetivo é verificar se a pergunta menciona explicitamente **dois ou mais cursos universitários pelo NOME COMPLETO** (por exemplo: 'Engenharia Civil', 'Medicina', 'Ciência da Computação', etc.).

✅ **REGRAS CLARAS QUE DEVEM SER OBEDECIDAS**:

1. **SÓ reformule** se houver **mais de um curso mencionado PELO NOME**.
   - Exemplo correto para reformular: "Qual a duração de Medicina e Direito na USP?"
   - Exemplo que NÃO deve ser reformulado: "computação código?", "Quantos cursos tem a UFCG?", "Quais cursos são ofertados?", etc.

2. **NÃO reformule** se a pergunta for ambígua, incompleta ou não mencionar cursos de forma clara.
   - Evite inferir ou completar com nomes de cursos se eles não estiverem escritos.
   - Palavras como "cursos", "faculdades", "carreiras" ou "áreas" sem especificação não são suficientes para disparar reformulação.

3. NÃO invente, NÃO corrija e NÃO interprete além do que está escrito.

---

🔁 Mesmo que **nenhuma reformulação seja necessária**, retorne a pergunta original no seguinte formato:

Pergunta reformulada: `pergunta reformulada aqui`

---

Agora, avalie e reformule (se necessário) a seguinte pergunta:

Pergunta: {question}
"""


class AgenteCursos(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)

    def processa_entrada_node(self, state: AgentState):
        if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")

        prompt_template = PromptTemplate(template=template, input_variables=["question"])

        #llm = HuggingFaceEndpoint(repo_id="maritaca-ai/sabia-7b", task="text-generation", temperature=0.1)
        #llm = ChatOllama(model="llama3.1:8b-instruct-q5_K_M", temperature=0)
        llm = ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
        llm_chain = prompt_template | llm

        messages = state["messages"]
        question = messages[0].content
        print("PERGUNTA ORIGINAL: ", question)
        response = llm_chain.invoke({"question": question})
        print("PERGUNTA REFEITA: ", response.content)
        match = re.search(r"(?i)Pergunta (?:refeita|reformulada):\s*(.+)", response.content.strip(), re.DOTALL)
        response_text = match.group(1).strip() if match else ""
        human_msg_id = messages[-1].id
        return {'messages': [HumanMessage(content=response_text, id=human_msg_id)]}
        # print("PERGUNTA REFEITA: ", response)
        # response_text = re.sub(r"^Resposta:\s*", "", response.strip())
        # human_msg_id = messages[-1].id
        # return {'messages': [HumanMessage(content=response_text, id=human_msg_id)]}

    def build(self):
        workflow = StateGraph(AgentState)
        #workflow.add_node("input", self.processa_entrada_node)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tools)
        workflow.add_node("exit", self.exit_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.should_continue, ["tools", "exit"])
        #workflow.add_edge("input", "agent")
        workflow.add_edge("tools", "agent")
        workflow.add_edge("exit", END)
        return workflow.compile()
    
    """def run(self, question: str):
        thread = {"configurable": {"thread_id": "1"}}
        '''output_file = "grafo.png"
        graph_image = self.app.get_graph().draw_mermaid_png()

        with open(output_file, "wb") as f:
            f.write(graph_image)'''
        
        for message_chunk, metadata in self.app.stream({"messages": [HumanMessage(content=question)]}, thread, stream_mode="messages"):
            if message_chunk.content:
                print(message_chunk.content, end="", flush=True)"""