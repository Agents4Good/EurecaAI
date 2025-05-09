from typing import Annotated, TypedDict
import uuid
from langgraph.prebuilt import ToolNode

from .agent_disciplinas import AgenteDisciplinas
from .agent_cursos import AgenteCursos
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage



def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid.uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]


class AgenteSupervisor:

    def __init__(self, LLM, model: str, prompt: str, temperatura: int = 0):
        self.model = LLM(model=model, temperature=temperatura)
        self.prompt = prompt
        self.app = self.build()

    
    def call_model(self, state: AgentState):
        messages = state["messages"]
        message = self.model.invoke(messages)

        print("MESSAGE: ", message)   

    
    def build(self):
        # Define the state graph
        workflow = StateGraph(AgentState)
        workflow.add_node("AgenteSupervisor", self.call_model)
        workflow.add_node("AgenteDisciplinas", AgenteDisciplinas)
        workflow.add_node("AgenteCursos", AgenteCursos)
        
        # Connect the nodes
        workflow.add_edge(START, "AgenteSupervisor")
        workflow.add_edge("AgenteSupervisor", "AgenteDisciplinas")
        workflow.add_edge("AgenteSupervisor", "AgenteCursos")
       
        # Define the exit node

        
        return workflow

    
