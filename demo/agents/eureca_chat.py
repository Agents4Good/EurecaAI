import operator, functools, asyncio
from typing import TypedDict, Annotated, Sequence, Optional

from langgraph.graph import StateGraph, END
from langgraph.types import Checkpointer
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from .create_agent import CreateAgent

from ..prompts.supervisor_prompt import SUPERVISOR_PROMPT
from ..prompts.aggregator_prompt import AGGREGATOR_PROMPT, AGGREGATOR_PROMPT_INFORMAL
from ..prompts.curso_prompt import CURSO_PROMPT
from ..prompts.disciplina_prompt import DISCIPLINA_PROMPT
from ..prompts.estudante_prompt import ESTUDANTE_PROMPT
from ..prompts.setor_prompt import SETOR_PROMPT

from tests.tools.curso import *
from tests.tools.disciplina import *
from tests.tools.estudante import *
from tests.tools.setor import *
from tests.tools.setor import *

from ..utils.supervisor_utils import *

from tests.tools.campus.get_calendarios import get_calendarios
from tests.tools.campus.get_campi import get_campi
from tests.tools.campus.get_periodo_mais_recente import get_periodo_mais_recente

from tests.tools.setor.get_estagios import get_estagios

# TOOLS USADAS
CAMPUS_TOOLS = [
    get_campi,
    get_calendarios,
    get_periodo_mais_recente
]

SETOR_TOOLS = [
    get_estagios
]

CURSO_TOOLS = [
    obter_dados_de_curso_especifico, 
    obter_dados_de_todos_os_cursos,
    get_todos_curriculos_do_curso
]

DISCIPLINA_TOOLS = [
    get_disciplina_ofertadas_periodo,
    get_horarios_turmas_vagas_disciplina,
    get_matriculas_disciplina,
    get_plano_de_aulas,
    get_plano_de_curso_disciplina,
    get_pre_requisitos_disciplina,
    #get_disciplinas,
]

ESTUDANTE_TOOLS = [
    obter_dados_gerais_de_todos_estudantes,
    obter_ingressantes_sisu
]

SETOR_TOOLS = [
    get_estagios,
    get_professores_setor,
    get_todos_setores
]

# SETAR ESTADO DO GRAFO GERAL (SUPERVISOR)
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    config: dict
    # last_agent: Optional[str]
    # agent_repetition_count: int

# CRIAR INSTÂNCIA DE CHAT DO EURECA
class EurecaChat:
    """
    """

    def __init__(self, supervisor_model: BaseChatModel, aggregator_model: BaseChatModel, agents_model: BaseChatModel, checkpointer: Optional[Checkpointer] = None):
        # Modelos
        self.supervisor_model = supervisor_model
        self.aggregator_model = aggregator_model
        self.agents_model = agents_model

        # Memória
        self.checkpointer = checkpointer

        # Agentes Especializados:
        # Curso
        self.agent_curso = CreateAgent('Agente_Curso').create_with_tools(model=self.agents_model, prompt=CURSO_PROMPT, tools=CURSO_TOOLS)
        self.curso_node = functools.partial(self.agent_node, agent=self.agent_curso, name="Agente_Curso")

        # Disciplina
        self.agent_disciplina = CreateAgent('Agente_Disciplina').create_with_tools(model=self.agents_model, prompt=DISCIPLINA_PROMPT, tools=DISCIPLINA_TOOLS)
        self.disciplina_node = functools.partial(self.agent_node, agent=self.agent_disciplina, name="Agente_Disciplina")

        # Estudante
        self.agent_estudante = CreateAgent('Agente_Estudante').create_with_tools(model=self.agents_model, prompt=ESTUDANTE_PROMPT, tools=ESTUDANTE_TOOLS)
        self.estudante_node = functools.partial(self.agent_node, agent=self.agent_estudante, name="Agente_Estudante")

        # Setor
        self.agent_setor = CreateAgent('Agente_Setor').create_with_tools(model=self.agents_model, prompt=SETOR_PROMPT, tools=SETOR_TOOLS)
        self.setor_node = functools.partial(self.agent_node, agent=self.agent_setor, name="Agente_Setor")

    
    def supervisor_node(self, state: AgentState):
        """
        """

        query, formatted_responses = format_agent_responses(state["messages"])

        prompt_template = PromptTemplate(template=SUPERVISOR_PROMPT, 
                                         input_variables=["members", "query", "responses"])
        
        supervisor_chain = prompt_template | self.supervisor_model

        result = supervisor_chain.invoke({
            "members": MEMBERS,
            "query": query,
            "responses": formatted_responses
        })
        print(query)
        print(formatted_responses)
        print(result)
        next_agent = extract_next_agent(result)
        print("PRÓXIMO AGENTE: ", next_agent)

        # last_agent = state.get("last_agent", None)
        # repetition_count = state.get("agent_repetition_count", 0)

        # if next_agent == last_agent:
        #     repetition_count += 1
        # else:
        #     repetition_count = 1
        #     last_agent = next_agent
        
        # if repetition_count >= 3:
        #     print(f"Agente {next_agent} foi selecionado 3 vezes seguidas. Redirecionando para Agente_Agregador.")
        #     next_agent = "FINISH"
        #     repetition_count = 0

        return {
            #"messages": state["messages"],
            "next": next_agent
            # "last_agent": last_agent,
            # "agent_repetition_count": repetition_count
        }
    
    
    async def aggregator_node(self, state: StateGraph):
        """
        """
        config = state.get("config", {})
        callbacks = config.get("callbacks", [])
        for cb in callbacks:
            if hasattr(cb, 'emit'):
                await cb.emit("agregando", {})
                await cb.emit("status", {"resposta": "Agregando as informações, aguarde!"})
                await cb.emit("logos_sites", [
                    "https://www.google.com/s2/favicons?sz=64&domain=g1.globo.com",
                    "https://www.google.com/s2/favicons?sz=64&domain=cnn.com",
                    "https://www.google.com/s2/favicons?sz=64&domain=exame.com",
                    "https://www.google.com/s2/favicons?sz=64&domain=uol.com"
                ])
            break
        
        user_query = next(
            (msg.content for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)), 
            "No questions found."
        )
        
        agent_responses = "\n".join(
            msg.content for msg in state["messages"] if isinstance(msg, AIMessage)
        )

        prompt = [
            SystemMessage(content=AGGREGATOR_PROMPT),
            HumanMessage(content=(
                f"Por favor agregue a seguinte informação:\n\n"
                f"Pergunta do usuário: {user_query}\n\n"
                f"Respostas encontradas:\n{agent_responses}"
            )),
        ]
        print("PROMPT DO AGREGADOR: ", prompt)
        
        """
        response = self.aggregator_model.invoke(prompt, config={"callbacks": callbacks})
        """
        llm_google = ChatOllama(model="llama3.2:3b", streaming=True, callbacks=callbacks)
        response = await llm_google.ainvoke(prompt)
        
        print("RESPOSTA DO AGREGADOR: ", response)
        return {
            "messages": [
                AIMessage(content=response.content, name="Agente_Agregador")
            ]
        }
    
    async def agent_node(self, state: AgentState, agent, name: str):
        """
        """

        try:
            result = await agent.ainvoke(state)
            print("\nRESULTADO DO AGENTE: ", {"messages": [AIMessage(content=result["messages"][-1].content, name=name)]})
            if isinstance(result, dict) and "messages" in result:
                return {"messages": [AIMessage(content=result["messages"][-1].content, name=name)]}
            return {"messages": [AIMessage(content=str(result), name=name)]}
        except Exception as e:
            return {"messages": [AIMessage(content=f"Ocorreu um erro: {str(e)}", name=name)]}
    
    def build(self):
        """
        """

        workflow = StateGraph(AgentState)
        workflow.add_node("Agente_Supervisor", self.supervisor_node)
        workflow.add_node("Agente_Agregador", self.aggregator_node)
        workflow.add_node("Agente_Curso", self.curso_node)
        workflow.add_node("Agente_Disciplina", self.disciplina_node)
        workflow.add_node("Agente_Estudante", self.estudante_node)
        workflow.add_node("Agente_Setor", self.setor_node)

        for member in MEMBERS:
            workflow.add_edge(member, "Agente_Supervisor")
        workflow.add_edge("Agente_Agregador", END)

        conditional_map = {k: k for k in MEMBERS}
        conditional_map["FINISH"] = "Agente_Agregador"
        workflow.add_conditional_edges(
            "Agente_Supervisor",
            lambda x: x["next"],
            conditional_map
        )

        workflow.set_entry_point("Agente_Supervisor")

        return workflow.compile(checkpointer=self.checkpointer)