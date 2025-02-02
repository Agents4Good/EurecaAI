import strawberry
from typing import Optional

@strawberry.type
class Disciplina:
    codigo_da_disciplina: Optional[int]
    nome: Optional[str]
    carga_horaria_teorica_semanal: Optional[int]
    carga_horaria_pratica_semanal: Optional[int]
    quantidade_de_creditos: Optional[int]
    horas_totais: Optional[int]
    media_de_aprovacao: Optional[int]
    carga_horaria_teorica_minima: Optional[int]
    carga_horaria_pratica_minima: Optional[int]
    carga_horaria_teorica_maxima: Optional[int]
    carga_horaria_pratica_maxima: Optional[int]
    numero_de_semanas: Optional[int]
    codigo_do_setor: Optional[int]
    nome_do_setor: Optional[str]
    campus: Optional[int]
    nome_do_campus: Optional[str]
    status: Optional[str]
    contabiliza_creditos: Optional[str]
    tipo_de_componente_curricular: Optional[str]
    carga_horaria_extensao: Optional[int]



@strawberry.type
class HorarioDisciplina:
    turma: Optional[int]
    codigo_da_disciplina: Optional[int]
    nome_da_disciplina: Optional[str]
    codigo_do_setor: Optional[int]
    nome_do_setor: Optional[str]
    campus: Optional[int]
    nome_do_campus: Optional[str]
    quantidade_de_creditos: Optional[int]
    carga_horaria: Optional[int]
    periodo: Optional[str]
    dia: Optional[int]
    hora_de_inicio: Optional[str]
    hora_de_termino: Optional[str]
    codigo_da_sala: Optional[str]

@strawberry.type
class PreRequisitoDisciplina:
    codigo_do_curso: Optional[int]
    codigo_da_disciplina: Optional[int]
    codigo_do_curriculo: Optional[int]
    ordem_de_prioridade: Optional[int]
    tipo: Optional[str]
    condicao: Optional[int]
    operador: Optional[int]

