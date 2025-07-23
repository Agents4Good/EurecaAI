import functools
from typing import Optional

from langgraph.graph import StateGraph, END
from langgraph.types import Checkpointer
from langchain_core.messages import AIMessage, RemoveMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import PromptTemplate
from .create_agent import CreateAgent

from ..prompts.supervisor_prompt import SUPERVISOR_PROMPT, SUPERVISOR_PROMPT_V2
from ..prompts.aggregator_prompt import AGGREGATOR_PROMPT, AGGREGATOR_PROMPT_V2
from ..prompts.curso_prompt import CURSO_PROMPT
from ..prompts.disciplina_prompt import DISCIPLINA_PROMPT
from ..prompts.estudante_prompt import ESTUDANTE_PROMPT
from ..prompts.setor_prompt import SETOR_PROMPT

from ..utils.supervisor_utils import *
from ..utils.eureca_chat_utils import *


# CRIAR INSTÂNCIA DE CHAT DO EURECA
class EurecaChat:
    """
    """

    def __init__(self, supervisor_model: BaseChatModel, aggregator_model_class, aggregator_model_kwargs,
                 agents_model: BaseChatModel, summarizer_model: BaseChatModel = None, checkpointer: Optional[Checkpointer] = None):
        # Modelos
        self.supervisor_model = supervisor_model
        self.aggregator_model_class = aggregator_model_class
        self.aggregator_model_kwargs = aggregator_model_kwargs
        self.agents_model = agents_model
        self.summarizer_model = summarizer_model

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

        # Setor
        self.agent_setor = CreateAgent('Agente_Setor').create_with_tools(model=self.agents_model, prompt=SETOR_PROMPT, tools=SETOR_TOOLS)
        self.setor_node = functools.partial(self.agent_node, agent=self.agent_setor, name="Agente_Setor")

    
    async def summarizer_node(self, state: AgentState):
        """
        """

        messages = state["messages"]
        summary = state.get("summary", "")
        response_count = state.get("response_count", 0)
        limit = 3

        print("\nESTADO QUANDO CHECGOU NO SUMARIZADOR:\n", state)
        print("\nCONTAGEM DE RESPOSTAS GERADAS: ", response_count)

        latest_pair = format_context(messages)

        if response_count < limit:
            if summary:
                new_context = f"{summary.strip()}\n\n---\n\n{latest_pair}".strip()
            else:
                new_context = latest_pair
            print("\nCONTEXTO CAPTURADO:\n", new_context)
            return {
                "context": new_context,
                "summary": summary,
                "aggregator_response_count": response_count
            }
        
        try:
            text_to_summarize = format_context_to_summarize(messages)
            print("\nTEXTO QUE VAI SER USADO PARA RESUMIR A CONVERSA:\n", text_to_summarize)
            prompt = (
                f"Resuma o histórico de conversa a seguir, mantendo as informações importantes:\n\n{text_to_summarize}\n\n"
                "*IMPORTANTE*:\n"
                "- O resumo deve manter a essência das perguntas e respostas e não deve ser longo.\n"
                "- Seja direto e evite repetições.\n"
                "- Se atente a informações importantes, essas informações não devem ficar de fora.\n"
                "- Use o formato: Resumo: <seu resumo aqui>"
            )
            response = await self.summarizer_model.ainvoke(prompt)
            new_summary = response.content.strip()
            new_context = f"{new_summary}\n\n---\n\n{latest_pair}".strip()
            print("\nNOVO CONTEXTO CAPTURADO COM RESUMO:\n", new_context)
            deleted_msgs = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
            return {
                "messages": deleted_msgs,
                "context": new_context,
                "summary": new_summary,
                "response_count": 0
            }
        except Exception as e:
            print(f"[Erro no summarizer_node]: {e}")
            context = state.get("context", "")
            fallback_context = f"{context.strip()}\n\n---\n\n{latest_pair}".strip() if context else latest_pair
            return {
                "context": fallback_context,
                "response_count": response_count
            }


    async def supervisor_node(self, state: AgentState):
        """
        """

        query, formatted_responses = format_agent_responses(state["messages"])
        context = state.get("context", "").strip()

        prompt_template = PromptTemplate(template=SUPERVISOR_PROMPT_V2, 
                                         input_variables=["members", "context", "query", "responses"])
        
        supervisor_chain = prompt_template | self.supervisor_model

        result = await supervisor_chain.ainvoke({
            "members": MEMBERS,
            "context": context,
            "query": query,
            "responses": formatted_responses
        })
        print(result)
        formatted_prompt = prompt_template.format(
            members=MEMBERS,
            context=context,
            query=query,
            responses=formatted_responses
        )
        print(formatted_prompt)
        print("\nESTADO QUANDO CHECGOU NO SUPERVISOR:\n", state)
        next_agent = extract_next_agent(result)
        print("PRÓXIMO AGENTE: ", next_agent)

        # last_agent = state.get("last_agent", None)
        # repetition_count = state.get("agent_repetition_count", 0)

        # if next_agent == last_agent:
        #     repetition_count += 1
        # else:
        #     repetition_count = 1
        #     last_agent = next_agent
        
        # if repetition_count >= 3:
        #     print(f"Agente {next_agent} foi selecionado 3 vezes seguidas. Redirecionando para Agente_Agregador.")
        #     next_agent = "FINISH"
        #     repetition_count = 0

        return {
            #"messages": state["messages"],
            "next": next_agent
            # "last_agent": last_agent,
            # "agent_repetition_count": repetition_count
        }
    
    
    async def aggregator_node(self, state: StateGraph, config: RunnableConfig):
        """
        """

        callbacks = config["configurable"].get("callbacks_sio")

        aggregator_model = self.aggregator_model_class(callbacks=callbacks, **self.aggregator_model_kwargs)

        for cb in callbacks:
            if hasattr(cb, 'emit'):
                await cb.emit("agregando", {})
                await cb.emit("status", {"resposta": "Agregando as informações, aguarde!"})
                await cb.emit("logos_sites", [
                    "https://www.google.com/s2/favicons?sz=64&domain=g1.globo.com",
                    "https://www.google.com/s2/favicons?sz=64&domain=cnn.com",
                    "https://www.google.com/s2/favicons?sz=64&domain=exame.com",
                    "https://www.google.com/s2/favicons?sz=64&domain=uol.com"
                ])
            break
        
        query, formatted_responses = format_agent_responses(state["messages"])
        context = state.get("context", "").strip()

        prompt_template = PromptTemplate(template=AGGREGATOR_PROMPT_V2, 
                                         input_variables=["context", "query", "responses"])

        aggregator_chain = prompt_template | aggregator_model

        response = await aggregator_chain.ainvoke({
            "context": context,
            "query": query,
            "responses": formatted_responses
        })
        formatted_prompt = prompt_template.format(
            context=context,
            query=query,
            responses=formatted_responses
        )
        print(formatted_prompt)
        return {
            "messages": [
                AIMessage(content=response.content, name="Agente_Agregador")
            ],
            "response_count": state.get("response_count", 0) + 1
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

        workflow = StateGraph(AgentState, config_schema=ConfigSchema)
        workflow.add_node("Agente_Entrada", self.summarizer_node)
        workflow.add_node("Agente_Supervisor", self.supervisor_node)
        workflow.add_node("Agente_Agregador", self.aggregator_node)
        workflow.add_node("Agente_Curso", self.curso_node)
        workflow.add_node("Agente_Disciplina", self.disciplina_node)
        workflow.add_node("Agente_Estudante", self.estudante_node)
        workflow.add_node("Agente_Setor", self.setor_node)

        workflow.add_edge("Agente_Entrada", "Agente_Supervisor")
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

        workflow.set_entry_point("Agente_Entrada")
        #workflow.set_entry_point("Agente_Supervisor")

        return workflow.compile(checkpointer=self.checkpointer)