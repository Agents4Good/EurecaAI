import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE

def get_carga_horaria(nome_do_curso: Any, nome_do_campus: Any) -> dict:
    """
    Buscar a carga horária de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        Dicionário com 'carga_horaria_creditos_minima', 'carga_horaria_creditos_maxima', 'carga_horaria_disciplinas_obrigatorias_minima', 'carga_horaria_disciplinas_optativas_minima', 'carga_horaria_atividades_complementares_minima', 'carga_horaria_minima_total', tudo em horas.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    
    print(f"Tool get_carga_horaria chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    
    dados_curso = get_curso_most_similar(nome_do_curso, nome_do_campus)
    response = requests.get(f'{URL_BASE}/curriculos?curso={dados_curso["curso"]["codigo"]}')

    if response.status_code == 200:
        cargas = [
            'codigo_do_curriculo',
            'carga_horaria_creditos_minima',
            'carga_horaria_creditos_maxima',
            'carga_horaria_disciplinas_obrigatorias_minima',
            'carga_horaria_disciplinas_optativas_minima',
            'carga_horaria_atividades_complementares_minima',
            'carga_horaria_minima_total'
        ]
        result = json.loads(response.text)[-1]
        return {key: result[key] for key in cargas}
    else:
        return {"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}