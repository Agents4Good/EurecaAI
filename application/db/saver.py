from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

def get_postgres_saver(db_uri: str):
    """
    Retorna instância do PostgresSaver Assíncrono
    """

    return AsyncPostgresSaver.from_conn_string(db_uri)