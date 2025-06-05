import uuid, json, re
from typing import Sequence, TypedDict, Annotated, Any, cast
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph
from langchain_core.messages import AnyMessage, SystemMessage, AIMessage
from langchain_core.language_models import BaseChatModel, LanguageModelLike
from langgraph.prebuilt.tool_executor import ToolExecutor
from langchain_core.tools import BaseTool

def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    for message in right:
        if not message.id:
            message.id = str(uuid.uuid4())
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            merged.append(message)
    return merged

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]
    user_token: dict[str, Any]

class CreateAgent():

    def __init__(self, name: str):
        self.name = name

    def create_with_tools(self, model: LanguageModelLike, prompt: str, tools: list, checkpointer = None) -> CompiledGraph:
        """
        Cria um agente com tools. O agente criado é um grafo compatível com ChatModel.

        Args:
            model: ChatModel que tenha suporte a tool calling.
            prompt: Prompt utilizado pelo agente.
            tools: Uma lista de tools no formato compatível com o langchain.
            checkpointer: Usado para persistir o estado do grafo para uma única thread.
        
        Returns:
            Um grafo compilado que poderá ser usado para interações de chat.
        """

        try:
            if isinstance(tools, ToolExecutor):
                tool_classes = Sequence[BaseTool] = tools.tools
                tool_node = ToolNode(tool_classes)
            else:
                tool_node = ToolNode(tools)
                tool_classes = list(tool_node.tools_by_name.values())
        except Exception as e:
            print(f"Erro ao adicionar as tools ao agente: {e}")
        
        model = cast(BaseChatModel, model).bind_tools(tool_classes)

        def call_model(state: AgentState):
            messages = state["messages"]
            filtered_messages = [
                msg for msg in messages
                if not isinstance(msg, AIMessage) or getattr(msg, 'name', None) == self.name or getattr(msg, 'name', None) is None
            ]
            
            if prompt:
                messages = [SystemMessage(content=prompt)] + messages
                filtered_messages = [SystemMessage(content=prompt)] + filtered_messages

            response = model.invoke(filtered_messages)
            response = extract_tool_calls(response)

            print("RESPONSE COM O THINK: ", response)
            if hasattr(response, "content") and isinstance(response.content, str):
                response.content = re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL).strip()
            print("RESPONSE SEM O THINK: ", response)

            return {'messages': [AIMessage(content=response.content, tool_calls=response.tool_calls)]}
        
        def extract_tool_calls(response):
            try:
                content_data = json.loads(response.content)
                if "tool_calls" in content_data:
                    tool_calls = content_data["tool_calls"]

                    for tool_call in tool_calls:
                        tool_call.setdefault("id", str(uuid.uuid4()))
                        tool_call.setdefault("type", "tool_call")
                    
                    response.tool_calls = tool_calls
                    response.content = content_data.get("content", "")
            
            except json.JSONDecodeError:
                pattern = r"<function=([a-zA-Z_][a-zA-Z0-9_]*)>\s*(\{.*?\})(?:\s*;)?"
                matches = re.findall(pattern, response.content)

                tool_calls = []
                for func_name, args_json in matches:
                    try:
                        args = json.loads(args_json)
                        tool_call = {
                            "name": func_name,
                            "args": args,
                            "id": str(uuid.uuid4()),
                            "type": "tool_call"
                        }
                        tool_calls.append(tool_call)
                    except json.JSONDecodeError:
                        continue
                
                if tool_calls:
                    response.tool_calls = tool_calls
                    response.content = ""
                    response.response_metadata["finish_reason"] = "tool_calls"
            return response
        
        def should_continue(state: AgentState):
            messages = state["messages"]
            last_message = messages[-1]
            if last_message.tool_calls:
                return "tools"
            else:
                return "__end__"
        
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")

        return workflow.compile(checkpointer=checkpointer)