import requests
from ..utils.base_url import URL_BASE
import json
from collections import defaultdict

def get_turmas_por_cursos(codigo_da_disciplina: int, turma: str, periodo: str) -> dict:
    """Obtém as vagas reservadas por curso em uma turma específica ou em todas as turmas"""

    params = {
        "disciplina": codigo_da_disciplina,
        "periodo-de": periodo,
        "periodo-ate": periodo
    }
    
    response = requests.get(f"{URL_BASE}/turmas-por-cursos", params=params)
    if response.status_code != 200:
        return {"status_code": response.status_code, "msg": response.json()}

    turmas = json.loads(response.text)

    vagas_por_curso = defaultdict(lambda: {
        "vagas_disponiveis": 0,
        "vagas_totais": 0,
        "vagas_preenchidas": 0
    })

    for turma_info in turmas:
        if turma and str(turma_info.get("turma")) != str(turma):
            continue  # filtra se o valor de 'turma' foi fornecido

        for vaga in turma_info.get("vagas", []):
            cod_curso = vaga["codigo_do_curso"]
            disponiveis = vaga.get("vagas_disponiveis") or 0
            totais = vaga.get("vagas_totais") or 0
            preenchidas = totais - disponiveis

            vagas_por_curso[cod_curso]["vagas_disponiveis"] += disponiveis
            vagas_por_curso[cod_curso]["vagas_totais"] += totais
            vagas_por_curso[cod_curso]["vagas_preenchidas"] += preenchidas

    resultado = []
    for codigo_do_curso, dados in vagas_por_curso.items():
        curso_resp = requests.get(f"{URL_BASE}/cursos", params={"curso": codigo_do_curso})
        if curso_resp.status_code == 200:
            curso = json.loads(curso_resp.text)
            descricao = curso[0].get("descricao", "Curso desconhecido") if isinstance(curso, list) and curso else "Curso desconhecido"
            resultado.append({
                "ofertadas_para": descricao,
                "vagas_totais": dados["vagas_totais"],
                "vagas_disponiveis": dados["vagas_disponiveis"],
                "vagas_preenchidas": dados["vagas_preenchidas"],
            })
    
    todas_ofertas = {
        "vagas_totais_geral": 0,
        "vagas_disponiveis_geral": 0,
        "vagas_totais_preenchidas_geral": 0
    }
    for oferta in resultado:
        todas_ofertas["vagas_totais_geral"] += oferta["vagas_totais"]
        todas_ofertas["vagas_disponiveis_geral"] += oferta["vagas_disponiveis"]
        todas_ofertas["vagas_totais_preenchidas_geral"] += oferta["vagas_preenchidas"]
    todas_ofertas["ofertas_para_os_cursos"] = resultado

    return todas_ofertas

#print(get_turmas_por_cursos(1411171, turma="", periodo="2024.1"))