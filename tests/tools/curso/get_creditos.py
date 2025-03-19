import json
import requests
from typing import Any
from .utils import get_curso_most_similar
from ..utils.base_url import URL_BASE

def get_creditos(nome_do_curso: Any, nome_do_campus: Any) -> dict:
    """
    Buscar os créditos de um curso.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        Dicionário com 'minimo_creditos_disciplinas_obrigatorias', 'minimo_creditos_disciplinas_optativas', 'minimo_creditos_atividades_complementares', 'minimo_creditos_total'.
    """
    
    nome_do_curso=str(nome_do_curso)
    nome_do_campus=str(nome_do_campus)
    
    print(f"Tool get_creditos chamada com nome_do_curso={nome_do_curso} e nome_do_campus={nome_do_campus}.")
    
    dados_curso = get_curso_most_similar(nome_do_curso, nome_do_campus)
    response = requests.get(f'{URL_BASE}/curriculos?curso={dados_curso["curso"]["codigo"]}')

    if response.status_code == 200:
        cargas = [
            'codigo_do_curriculo',
            'minimo_creditos_disciplinas_obrigatorias',
            'minimo_creditos_disciplinas_optativas',
            'minimo_creditos_atividades_complementares',
            'minimo_creditos_total'
        ]
        result = json.loads(response.text)[-1]
        return {key: result[key] for key in cargas}
    else:
        return {"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}