import requests, json, inspect, time, traceback

from functools import wraps

from ..utils.base_url import URL_BASE
from .get_todos_setores import get_todos_setores, get_todos_setores_por_codigo_do_campus
from ..utils.most_similar import get_most_similar
from ..utils.processar_json import processar_json
from application.config import model


format = """{'setor': {'codigo': '', 'nome': ''}}"""
mapper_setor = {"nome": "descricao", "codigo": "codigo_do_setor"}

def get_setor_most_similar(nome_do_centro_setor: str, nome_do_campus: str, filtro: str = "") -> dict:
    """
    Busca o código do setor pelo nome dele.

    Args:
        nome_do_centro_setor: nome do setor.
        nome_do_campus: O parâmetro nome_do_campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (se o campus não foi informado, retorne uma mensagem de erro pois, precisa do campus).
        filtro: usar 'UNID' ou 'CENTRO'. (se não foi informado, ou se perguntar pelo setor, então use a string vazia '').

    Returns:
        dict: dicionário contendo código e o nome do setor.
    """
    print(f"`get_setor_most_similar` chamado com nome_do_centro_setor={nome_do_centro_setor}, nome_do_campus={nome_do_campus}, filtro={filtro}")
    
    setores_campus = get_todos_setores(nome_do_campus=nome_do_campus, filtro="UNID")
    setores_filtrados = [setor for setor in setores_campus if filtro.lower() in setor["descricao"].lower()]
    setor_most_similar, _ = get_most_similar(lista_a_comparar=setores_filtrados, dado_comparado=nome_do_centro_setor, top_k=5, mapper=mapper_setor, limiar=0.65)
    
    response = model.invoke(
        f"""
        Para o setor de nome: '{nome_do_centro_setor}', quais desses possíveis cursos abaixo é mais similar ao campus do nome informado?
        
        {setor_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    
    return processar_json(response.content, "setor")


def get_setor_most_similar_por_codigo(nome_do_centro_setor: str, codigo_do_campus: str, filtro: str = "") -> dict:
    """
    Busca o código do setor pelo nome dele.

    Args:
        nome_do_centro_setor: nome do setor.
        codigo_do_campus: código do campus(se o campus não foi informado, retorne uma mensagem de erro pois, precisa do campus).
        filtro: usar 'UNID' ou 'CENTRO'. (se não foi informado, ou se perguntar pelo setor, então use a string vazia '').

    Returns:
        dict: dicionário contendo código e o nome do setor.
    """
    print(f"`get_setor_most_similar_por_codigo_do_campus` chamado com nome_do_centro_setor={nome_do_centro_setor}, codigo_do_campus={codigo_do_campus}, filtro={filtro}")
    
    setores_campus = get_todos_setores_por_codigo_do_campus(codigo_do_campus=codigo_do_campus, filtro="UNID")
    setores_filtrados = [setor for setor in setores_campus if filtro.lower() in setor["descricao"].lower()]
    setor_most_similar, _ = get_most_similar(lista_a_comparar=setores_filtrados, dado_comparado=nome_do_centro_setor, top_k=5, mapper=mapper_setor, limiar=0.65)
    
    response = model.invoke(
        f"""
        Para o setor de nome: '{nome_do_centro_setor}', quais desses possíveis cursos abaixo é mais similar ao campus do nome informado?
        
        {setor_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        """
    )
    
    return processar_json(response.content, "setor")


def obter_disciplina_codigo(codigo: int):
    """
    Obtém informações sobre uma disciplina a partir do seu código.

    Args:
        codigo (str): Código da disciplina.

    Returns:
        dict: Informações sobre a disciplina.
    """

    params = {
        'disciplina': codigo
    }

    url = f"{URL_BASE}/disciplinas"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return {"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}


def logger_eureca_tool(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()

        argumentos_formatados = [
            f'{k}="{v}"' if isinstance(v, str) else f"{k}={v}"
            for k, v in bound_args.arguments.items()
        ]

        argumentos_str = ",\n\t- ".join(argumentos_formatados)
        print(f"Tool {func.__name__} chamada com os seguintes parâmetros:\n\t- {argumentos_str}")

        argumentos = {
            k: v for k, v in bound_args.arguments.items()
            if v not in ("", None)
        }

        inicio = time.time()

        try:
            retorno = func(*args, **kwargs)
        except Exception as error:
            print("\n❌ ERRO DURANTE A EXECUÇÃO DA FUNÇÃO. Arquivo e linha do erro:")
            print(traceback.format_exc())
            return str(error)

        fim = time.time()
        tempo_execucao = fim - inicio

        result = {
            "nome_da_funcao": func.__name__,
            "resposta": retorno,
            "Argumentos_usados": argumentos,
            "tempo_execucao_segundos": round(tempo_execucao, 4)
        }

        query = argumentos.get("query", None)
        if query is not "" and query is not None:
            print(json.dumps(result, indent=4, ensure_ascii=False))
            return result

        return retorno

    return wrapper