import strawberry
from typing import Optional

@strawberry.type
class Turma:
    turma: Optional[int]
    codigo_da_disciplina: Optional[int]
    periodo: Optional[str]
    numero_de_notas: Optional[int]
    quantidade_de_creditos: Optional[int]
    carga_horaria: Optional[int]
    tipo: Optional[str]
