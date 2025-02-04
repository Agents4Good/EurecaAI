from typing import Optional
import strawberry

@strawberry.type
class Setor:
    codigo_do_setor: Optional[int]
    descricao: Optional[str]
    campus: Optional[int]
    email: Optional[str]