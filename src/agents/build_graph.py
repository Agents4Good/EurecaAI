from dotenv import load_dotenv

from .agent_state import AgentState
from .custom_agents import *
from .general_agents import *
from .agent_members import MEMBERS

from langgraph.graph import StateGraph, END

load_dotenv()

def detect_loop(state):
    """
    Detects whether the supervisor is trying to call the same agent repeatedly.
    """
    last_agents = [msg.name for msg in state["messages"][-2:]]  # Últimos dois agentes
    return last_agents[0] == last_agents[1] if len(last_agents) > 1 else False

def build_flow() -> StateGraph:
    """
        Build the graph
    """
    workflow = StateGraph(AgentState)
    workflow.add_node("Agente_Cursos_Eureca", cursos_eureca_node)
    workflow.add_node("Agente_Disciplinas_Turmas_Eureca", disciplinas_eureca_node)
    workflow.add_node("Agente_Campus_Eureca", campus_eureca_node)
    workflow.add_node("Agente_Setor_Professor_Estagio_Eureca", setor_node)
    workflow.add_node("Agente_Detector", detector_node)
    workflow.add_node("Agente_Agregador", aggregator_node)
    workflow.add_node("Agente_Supervisor", supervisor_node)

    for member in MEMBERS:
        workflow.add_edge(member, "Agente_Supervisor")
    workflow.add_edge("Agente_Agregador", END)
    
    conditional_map = {k: k for k in MEMBERS}
    conditional_map["FINISH"] = "Agente_Agregador"
    conditional_map["LOOP_DETECTED"] = "Agente_Agregador"
    workflow.add_conditional_edges(
        "Agente_Supervisor",
        lambda x: "LOOP_DETECTED" if detect_loop(x) else x["next"],
        conditional_map
    )
    
    workflow.set_entry_point("Agente_Supervisor")

    return workflow

def build():
    """
    Constructs the agent flow and compiles it.
    """
    workflow = build_flow()
    return workflow.compile()