from dotenv import load_dotenv

from ..prompts.system_prompts import SUPERVISOR_SYSTEM_PROMPT, AGGREGATOR_SYSTEM_PROMPT
from .agent_members import *
from .agent_state import RouteResponse

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

model = ChatOpenAI(model="gpt-4o")
#model = ChatOllama(model="llama3.2")

'''CLASSIFIER = pipeline(
    "zero-shot-classification",
    model='facebook/bart-large-mnli',
    hypothesis_template="Verifique em qual tópico o texto acima melhor se adequa: {}.",
    multi_label=True,
)'''

def supervisor_node(state):
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
    messages = [
        ("system", AGGREGATOR_SYSTEM_PROMPT),
        (
            "assistant",
            "Por favor agregue a seguinte informação:\n\n"
            + "\n".join([msg.content for msg in state["messages"]]),
        ),
    ]
    response = model.invoke(messages)
    return {
        "messages": [
            AIMessage(content=response.content, name="Agente_Agregador")
        ]
    }