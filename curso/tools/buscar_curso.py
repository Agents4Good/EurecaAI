from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_curso(campus:Any, curso: Any) -> list[dict]:
    """
    Retorna um  curso específico oferecido em um campus específico da UFCG.

    Args:
        campus (Any): Código do campus. 
        curso (Any): Código do curso.

    Returns:
        list[dict]: Lista com um único curso no formato:
            {
                "codigo_do_curso": int,         # Código do curso
                "descricao": str,               # Nome e descrição do curso
                "status": str,                  # Status do curso (ex.: "ATIVO")
                "grau_do_curso": str,            # Grau (ex.: "GRADUACAO")
                "codigo_do_setor": int,          # Código do setor
                "nome_do_setor": str,            # Nome do setor responsável
                "campus": int,                   # Código do campus
                "nome_do_campus": str,           # Nome do campus
                "turno": str,                    # Turno de funcionamento (ex.: "Matutino")
                "periodo_de_inicio": str,        # Período letivo de início (ex.: "2017.1")
                "data_de_funcionamento": str,    # Data de início do funcionamento
                "codigo_inep": int,              # Código INEP do curso
                "modalidade_academica": str,     # Modalidade acadêmica (ex.: "BACHARELADO")
                "curriculo_atual": int,          # Ano do currículo vigente
                "area_de_retencao": int,         # Código da área de retenção
                "ciclo_enade": int               # Ciclo do ENADE
            }
    """

    params = {
        "campus": campus, 
        "curso": curso
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/cursos"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return "Não foi possível obter os cursos ou nenhum curso foi encontrado"
        return data
    
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise
        