from .agent_tools import AgentTools

class AgenteSetores(AgentTools):

    def __init__ (self, LLM, model: str, tools: list, prompt: str, temperatura: float = 0):
        super().__init__(LLM, model,tools, prompt, temperatura)
