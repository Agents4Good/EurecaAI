import json
import requests
from typing import Any
from collections import defaultdict
from ..utils.base_url import URL_BASE
from ..curso.utils import get_curso_most_similar
from ..campus.utils import get_campus_most_similar

def get_ingressantes_sisu(nome_do_curso: Any = "", nome_do_campus: Any = "", periodo: Any = "") -> list:
    """
    _summary_
    Busca a quantidade de ingressantes através do Sisu.
    Contém a quantidade de estudantes que ingressaram para cada e sem cotas. 
    Além disso, também é retornado o número total de ingressantes.
    Use essa ferramenta quando quiser o número de ingressantes (válido apenas para quantidades).

    Args:
        nome_do_curso (Any): nome do curso. Defaults to "".
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal.
        periodo (Any): Período do campus ou curso. Defaults to "".
    
    Returns:
        list: Retorna uma lista contendo a quantidade de ingressantes.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    periodo=str(periodo)
    
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo
    }
    
    if (nome_do_curso != "" and nome_do_campus != ""):
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params["curso"] = dados_curso['curso']['codigo']
        params["campus"] = dados_campus['campus']['codigo']
    elif (nome_do_curso == "" and nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params["campus"] = dados_campus['campus']['codigo']
    elif (nome_do_curso == "" and nome_do_campus == ""):
        pass
    else:
        return [{"error_status": 500, "msg": "Não foi possível obter a informação porque você informou um curso sem passar o campus dele."}]

    
    response = requests.get(f'{URL_BASE}/estudantes', params=params)
    if response.status_code == 200:
        dados = json.loads(response.text)
        if len(dados) == 1:
            return dados
        
        somas = defaultdict(int)
        campos_ignorados = {"periodo", "codigo_do_curso"}

        for item in dados:
            for chave, valor in item.items():
                if chave not in campos_ignorados:
                    somas[chave] += valor if isinstance(valor, (int, float)) else 0

        resultado_final = dict(somas)
        return [json.dumps(resultado_final, indent=2, ensure_ascii=False)]
    
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]