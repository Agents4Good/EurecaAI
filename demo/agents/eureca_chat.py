import operator, functools
from typing import TypedDict, Annotated, Sequence, Optional

from langgraph.graph import StateGraph, END
from langgraph.types import Checkpointer
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from .create_agent import CreateAgent

from ..prompts.supervisor_prompt import SUPERVISOR_PROMPT
from ..prompts.aggregator_prompt import AGGREGATOR_PROMPT, AGGREGATOR_PROMPT_INFORMAL
from ..prompts.curso_prompt import CURSO_PROMPT
from ..prompts.disciplina_prompt import DISCIPLINA_PROMPT
from ..prompts.estudante_prompt import ESTUDANTE_PROMPT



from tests.tools.curso import *
from tests.tools.disciplina import *
from tests.tools.estudante import *

from ..utils.supervisor_utils import *

# TOOLS USADAS
CURSO_TOOLS = [
    obter_dados_de_curso_especifico, 
    obter_dados_de_todos_os_cursos,
]

DISCIPLINA_TOOLS = [
    #get_disciplina_ofertadas_periodo,
    get_horarios_disciplina,
    get_matriculas_disciplina,
    get_plano_de_aulas,
    get_plano_de_curso_disciplina,
    get_pre_requisitos_disciplina,
    get_disciplinas,
    #get_turmas_disciplina,
]

ESTUDANTE_TOOLS = [
    obter_dados_gerais_de_todos_estudantes
]

# SETAR ESTADO DO GRAFO GERAL (SUPERVISOR)
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

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

    
    def supervisor_node(self, state: AgentState):
        """
        """

        query, formatted_responses = format_agent_responses(state["messages"])

        # output_parser, format_instructions = get_supervisor_output_parser()

        # prompt_template = PromptTemplate(template=SUPERVISOR_PROMPT + "\n\n{format_instructions}", 
        #                                  input_variables=["members", "query", "responses"], 
        #                                  partial_variables={"format_instructions": format_instructions})
        
        # supervisor_chain = prompt_template | self.supervisor_model | output_parser

        # filled_prompt = prompt_template.format(
        #     members=MEMBERS,
        #     query=query,
        #     responses=formatted_responses
        # )
        # print("\nPROMPT DO SUPERVISOR: ", filled_prompt)
        # result = supervisor_chain.invoke({
        #     "members": MEMBERS,
        #     "query": query,
        #     "responses": formatted_responses
        # })

        # print("\nRESPOSTA DO SUPERVISOR: ", result)

        prompt_template = PromptTemplate(template=SUPERVISOR_PROMPT, 
                                         input_variables=["members", "query", "responses"])
        
        supervisor_chain = prompt_template | self.supervisor_model

        result = supervisor_chain.invoke({
            "members": MEMBERS,
            "query": query,
            "responses": formatted_responses
        })
        print(result)
        next_agent = extract_next_agent(result)
        print("PRÓXIMO AGENTE: ", next_agent)
        return {
            "messages": state["messages"],
            "next": next_agent
        }
    
    
    def aggregator_node(self, state: StateGraph):
        """
        """

        user_query = next(
            (msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)), 
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
        response = self.aggregator_model.invoke(prompt)
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




