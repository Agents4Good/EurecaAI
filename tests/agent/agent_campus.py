import json
import uuid
import ast
from .agent_tools import AgentTools

class AgenteCampus(AgentTools):
    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)