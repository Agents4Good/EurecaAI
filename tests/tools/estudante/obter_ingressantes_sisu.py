import json
import requests
from typing import Any
from collections import defaultdict
from ..utils.base_url import URL_BASE
from ..curso.utils import get_curso_most_similar
from ..campus.utils import get_campus_most_similar
from ..campus.get_periodo_mais_recente import get_periodo_mais_recente

def get_ingressantes_sisu(nome_do_curso: Any = "", nome_do_campus: Any = "", periodo: Any = "") -> list:
    """
    _summary_
    Busca a quantidade de ingressantes através do Sisu.
    Contém a quantidade de estudantes que ingressaram para cada e sem cotas. 
    Além disso, também é retornado o número total de ingressantes.
    Use essa ferramenta quando quiser o número de ingressantes (válido apenas para quantidades).

    Significado dos dados retornados são
    A0: Ampla Concorrência.
    L1: Candidatos com Renda Familiar Bruta per capita igual ou inferior a 1,5 Salário Mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L2: Candidatos autodeclarado pretos, pardos ou indígenas, com Renda Familiar Bruta per capita igual ou inferior a 1,5 Salário Mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L5: Candidatos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L6: Candidatos autodeclarado pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L9: Candidatos com deficiência com Renda Familiar Bruta per capita igual ou inferior a 1,5 Salário Mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L10: Candidatos com deficiência autodeclarado pretos, pardos ou indígenas, com Renda Familiar Bruta per capita igual ou inferior a 1,5 Salário Mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L13: Candidatos com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012).
    L14: Candidatos com deficiência autodeclarado pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei. 12.711/2012). 

    Args:
        nome_do_curso (Any): nome do curso. Defaults to "".
        nome_do_campus (Any): Cidade do campus, e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé e Pombal. Se não souber, usar Campina Grande como padrão.
        periodo (Any): Período do campus ou curso. Defaults to "".
    
    Returns:
        list: Retorna uma lista contendo a quantidade de ingressantes.
    """
    
    print(f"Tool get_ingressantes_sisu chamada com nome_do_campus={nome_do_campus}, nome_do_curso={nome_do_curso} e período={periodo}")

    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    periodo=str(periodo)
    
    if periodo == "":
        periodo = get_periodo_mais_recente()

    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo
    }
    
    if (nome_do_curso != "" and nome_do_campus != ""):
        dados_curso = get_curso_most_similar(nome_do_curso=nome_do_curso, nome_do_campus=nome_do_campus)
        params["curso"] = dados_curso['curso']['codigo']
    elif (nome_do_curso == "" and nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params["campus"] = dados_campus['campus']['codigo']
    elif (nome_do_curso == "" and nome_do_campus == ""):
        pass
    else:
        return [{"error_status": 500, "msg": "Não foi possível obter a informação porque você informou um curso sem passar o campus dele."}]

    
    response = requests.get(f'{URL_BASE}/vagas-no-sisu', params=params)
    if response.status_code == 200:
        dados = json.loads(response.text)
        if len(dados) == 1:
            return dados
        
        somas = defaultdict(int)
        campos_ignorados = {"periodo", "codigo_do_curso"}

        for item in dados:
            for chave, valor in item.items():
                if chave not in campos_ignorados:
                    if isinstance(valor, (int, float)) and valor is not None:
                        somas[chave] += valor

        resultado_final = dict(somas)
        return [json.dumps(resultado_final, indent=2, ensure_ascii=False)]
    
    else:
        return [{"error_status": response.status_code, "msg": response.json()}]