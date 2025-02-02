import strawberry
from datetime import datetime

@strawberry.type
class Aula:
    turma: int
    codigo_da_disciplina: int
    periodo: str
    aula_sequencia: int
    data: datetime
    horas: int
    assunto: str
