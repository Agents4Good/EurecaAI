import json
import uuid
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from .agent_tools import AgentTools, AgentState
from langgraph.graph import StateGraph, MessagesState, START, END


import ast
#tools

from langchain_ollama import ChatOllama

class AgenteCampus(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)
