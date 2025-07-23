from langgraph.checkpoint.base import BaseCheckpointSaver

from application.config import supervisor_model, aggregator_model_class, aggregator_model_kwargs, summarizer_model, agents_model
from demo.agents.eureca_chat import EurecaChat

def build_system(saver: BaseCheckpointSaver):
    """
    Constrói instância do EurecaChat com checkpointer
    """
    
    return EurecaChat(
        supervisor_model=supervisor_model,
        aggregator_model_class=aggregator_model_class,
        aggregator_model_kwargs=aggregator_model_kwargs,
        summarizer_model=summarizer_model,
        agents_model=agents_model,
        checkpointer=saver
    ).build()