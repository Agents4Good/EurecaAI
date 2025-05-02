from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE
from ..utils.most_similar import get_sim_course_name
import requests
import json

from langchain_core.tools import tool

@tool
def obter_dados_de_curso_especifico(nome_do_curso: Any, nome_do_campus: Any) -> list:
    """
    Buscar informação de um curso específico da UFCG a partir do nome do curso.

    Args:
        nome_do_curso: nome referente a apenas um curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... esse parâmetro não é obrigatório, se o campus não for fornecido use vazio ''.

    Returns:
        Lista com informações relevantes do curso específico, como código do curso, código do inep, código e nome do setor desse curso, período de início, etc.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    print(f"Tool get_curso chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")

    try:
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        if 'AskHuman' in dados_curso:
            return dados_curso
        if get_sim_course_name(nome_do_curso, dados_curso['curso']['nome']) < 0.5:
            print(get_sim_course_name(nome_do_curso, dados_curso['curso']['nome']))
            print(dados_curso['curso']['nome'])
            return [{"Error": f"Nenhum curso encontrado com o nome {nome_do_curso}"}]
    except ValueError as e:
        return [{"Error": str(e)}]

    params = { 
        'status-enum': 'ATIVOS',
        'curso': dados_curso['curso']['codigo']
    }
    response = requests.get(f'{URL_BASE}/cursos', params=params)

    if response.status_code == 200:
        #return [{**{k: v for k, v in item.items() if k != "descricao"}, "nome_do_curso": item["descricao"]} for item in json.loads(response.text)]
        return json.loads(response.text)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]