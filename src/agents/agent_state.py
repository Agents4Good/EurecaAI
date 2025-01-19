import operator

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from .agent_members import OPTIONS

class RouteResponse(BaseModel):
    next: Literal[OPTIONS]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str