import json
import uuid
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from .agent_tools import AgentTools
from langgraph.graph import StateGraph, MessagesState, START, END


class AgenteCursos(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)

