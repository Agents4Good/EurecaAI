import json
import uuid
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from .agent_tools import AgentTools, AgentState
from langgraph.graph import StateGraph, MessagesState, START, END


import ast
#tools
from ..tools.disciplina.utils import get_most_similar
from ..tools.disciplina.get_todas_disciplinas_curso import get_todas_disciplinas_curso


from langchain_ollama import ChatOllama

class AgenteDisciplinas(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)

    def processa_entrada_rag_node(self, state: AgentState):
        pass


    # def build(self):
    #     workflow = StateGraph(AgentState)
    #     #workflow.add_node("processa_entrada", self.processa_entrada_rag_node)
    #     workflow.add_node("agent", super().call_model)
    #     workflow.add_node("tools", self.tools)
    #     workflow.add_edge(START, "agent")
    #     #workflow.add_edge("processa_entrada","agent")
    #     workflow.add_conditional_edges("agent", super().should_continue, ["tools", END])
    #     workflow.add_edge("tools", "agent")
    #     return workflow.compile()