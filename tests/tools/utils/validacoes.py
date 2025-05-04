import re
from datetime import date
from ..campus.get_calendarios import get_calendarios
from ..curso.get_todos_curriculos_do_curso import get_todos_curriculos_do_curso

ano_inicio = 2017

def validar_periodo(periodo: str):
    padrao = r'^(20\d{2})\.(1|2)$'
    match = re.match(padrao, periodo)
    if match:
        ano = int(match.group(1))
        result = ano_inicio <= ano <= date.today().year
        if result: 
            print("-------- Período válido --------")
            return True, ""
    
    print("-------- Períoodo inválido --------")
    calendarios = get_calendarios()
    periodos = [calendario["periodo"] for calendario in calendarios]
    return False, f"Período inválido. Informe ao usuário que os períodos que ele pode acessar são {', '.join(periodos)} e que o período mais recente é o de {periodos[-1]}."


def validar_curriculo(curriculo_usado: str, nome_do_campus: str, nome_do_curso: str) -> bool:
    todos_curriculos = get_todos_curriculos_do_curso(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)
    curriculos = [curriculo["codigo_do_curriculo"] for curriculo in todos_curriculos]

    if curriculo_usado.isdigit() and len(curriculo_usado) == 4:
        ano = int(curriculo_usado)
        result = ano_inicio <= ano <= date.today().year and int(curriculo_usado) in curriculos
        if result:
            print("-------- Currículo válido --------")
            return result, ""
    
    print("-------- Currículo inválido --------")
    return False, f"Currículo inválido. Informe ao usuário que para o curso {nome_do_curso} existem apenas esses currículos {', '.join(str(c) for c in curriculos)} e que o mais recente é o currículo de {str(curriculos[-1])}"


def validar_turma(turma_usada: str):
    if (turma_usada.isdigit() and int(turma_usada) >= 1 and int(turma_usada) <= 20) or turma_usada == "": 
        return True, ""
    return False, f"Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é 1 (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema)."