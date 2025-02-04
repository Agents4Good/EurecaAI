from typing import Optional
import strawberry

@strawberry.type
class Professor:
    matricula_do_docente: Optional[int]
    codigo_do_setor: Optional[int]
    status: Optional[str]
    titulacao: Optional[str]