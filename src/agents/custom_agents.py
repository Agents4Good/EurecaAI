from dotenv import load_dotenv

from ..prompts.system_prompts import SUPERVISOR_SYSTEM_PROMPT, AGGREGATOR_SYSTEM_PROMPT
from .agent_members import *
from .agent_state import RouteResponse

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

model = ChatOpenAI(model="gpt-4o")
#model = ChatOllama(model="llama3.2")

def supervisor_node(state):
    """
        Agente supervisor encaminha a tarefa para o agente apropriado e analisa 
        se a pergunta do usuário já foi respondida.

        Args:
            state: Estado do grafo
        
        Returns:
            Resposta do modelo
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", SUPERVISOR_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Dado a conversa acima, analise o contexto e decida se a pergunta do usuário foi respondida. Caso ainda não foi respondida, decida qual agente deve ser chamado em seguida. "
            "Se tudo estiver resolvido, retorne 'FINISH'. Selecione apenas uma das opções: {options}."
            "Antes de selecionar, certifique-se de que a tarefa avançou. "
            "Se a mesma tarefa foi repetida ou parece redundante, retorne com 'FINISH'."
        )
    ]).partial(options=str(OPTIONS), members=", ".join(MEMBERS))

    supervisor_chain = prompt | model.with_structured_output(RouteResponse)
    result = supervisor_chain.invoke(state)
    return result

def aggregator_node(state):
    """
        Recebe um estado (state) com mensagens geradas por outros agentes, 
        envia essas informações para o modelo de linguagem e retorna uma resposta

        Args:
            state: Estado do grafo

        Returns:
            Resposta do modelo

    """
    user_query = next(
        (msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)), 
        "Nenhuma pergunta encontrada."
    )
    
    '''agent_responses = next(
        (msg.content for msg in state["messages"] if isinstance(msg, AIMessage)),
        "Nenhuma resposta encontrada."
    )'''
    agent_responses = "\n".join(
        msg.content for msg in state["messages"] if isinstance(msg, AIMessage)
    )
    
    messages = [
        ("system", AGGREGATOR_SYSTEM_PROMPT),
        (
            "assistant",
            f"Por favor agregue a seguinte informação:\n\n"
            f"Pergunta do usuário: {user_query}\n\n"
            f"Respostas encontradas:\n{agent_responses}"
        ),
    ]
    #print(state)
    #print("\n\n")
    #print(messages)
    response = model.invoke(messages)
    return {
        "messages": [
            AIMessage(content=response.content, name="Agente_Agregador")
        ]
    }