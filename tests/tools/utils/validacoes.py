import re
from datetime import date
from ..campus.get_calendarios import get_calendarios
from ..curso.get_todos_curriculos_do_curso import get_todos_curriculos_do_curso
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente
from ..curso.get_todos_curriculos_do_curso import get_todos_curriculos_do_curso
from ..curso.get_todos_curriculos_do_curso import get_todos_curriculos_do_curso_por_codigo
from ..curso.utils import get_curso_most_similar

ano_inicio = 2002

def validar_periodo(*periodos: str):
    padrao = r'^(20\d{2})\.(1|2)$'
    calendarios = get_calendarios()
    periodos_validos = [calendario["periodo"] for calendario in calendarios]
    
    for periodo in periodos:
        print(periodo)
        if periodo == "":
            continue
        match = re.match(padrao, periodo)
        if match:
            ano = int(match.group(1))
            result = ano_inicio <= ano <= date.today().year
            if not result: 
                return False, f"Período inválido. Informe ao usuário que os períodos que ele pode acessar são {', '.join(periodos_validos)} e que o período mais recente é o de {periodos_validos[-1]}. O formato é sempre 'Ano.X', onde X é um número."
    return True, ""


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
    return False, f"Turma inválida. A turma precisa ser um valor númerico entre 1 a 20. O padrão é vazio '' (caso você escolha o padrão, você deve informar ao usuário da sua escolha relatando o problema)."

def busca_curriculo_no_periodo(periodo: str, todos_curriculos: list):
    todos_curriculos = [curriculo["codigo_do_curriculo"] for curriculo in todos_curriculos]
    ano_periodo = int(periodo.split('.')[0])
    
    curriculos_ordenados = sorted(todos_curriculos)    
    curriculo_encontrado = None
    
    for curriculo in curriculos_ordenados:
        if int(curriculo) <= int(ano_periodo):
            curriculo_encontrado = curriculo
        else:
            break

    return curriculo_encontrado


def valida_periodo_curriculo(nome_do_campus: str, nome_do_curso: str, periodo: str, curriculo: str):
    mensagem = ""
    dados_curso = get_curso_most_similar(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso)

    if periodo == "":
        periodo = get_periodo_mais_recente()
    
    if curriculo == "":
        todos_curriculos = get_todos_curriculos_do_curso_por_codigo(codigo_do_curso=dados_curso["curso"]["codigo"])
        curriculo_atual = todos_curriculos[-1]
        if int(periodo.split(".")[0]) < int(curriculo_atual['codigo_do_curriculo']):
            curriculo = busca_curriculo_no_periodo(periodo=periodo, todos_curriculos=todos_curriculos)
            if curriculo == None:
                mensagem = "Erro: Informe ao usuário o curso não existia nesse período, portanto não é possível obter os dados da disciplina nesse período."
        else:
            curriculo = curriculo_atual["codigo_do_curriculo"]
    else:
        if int(periodo.split(".")[0]) < int(curriculo):
            mensagem = f"Erro: O período {periodo} não pode ser anterior ao curriculo de {curriculo}. Precisa ser igual ou superior."
    
    return dados_curso, curriculo, periodo, mensagem