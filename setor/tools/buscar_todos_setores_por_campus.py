from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info

@mcp.tool()
async def buscar_todos_setores_por_campus(campus:Any, tipo_setor: Any) -> list[dict]:
    """
    Retorna todos os setores de um campus específico da UFCG.

    Args:
        campus (Any): Código do campus. 
        tipo_setor(Any): tipo do setor. Valores permitidos:
            - 'DEPARTAMENTO'
            - 'ESCOLA'
            - 'PROGRAMA_POS_GRADUACAO'
            - 'CENTRO'
            - 'UNIDADE_ACADEMICO_ESPECIFICA'
            - 'COORDENACAO_CURSO'
            - 'REITORIA'
            - 'COORDENACAO_CURSO_LATO'
            - 'RESDIDENCIA_MEDICA'
            - 'COORDENACAO_POS_GRADUCAO' 
            

    Returns:
        list[dict]: Lista de setores no formato:
            {
                "codigo_do_setor": int,  # Código do setor
                "descricao": str,        # Nome ou descrição do setor
                "campus": int,           # Código do campus
                "email": str | None      # E-mail de contato do setor, se disponível
            }
    """

    params = {
        "campus": campus,
        "tipo_setor": tipo_setor
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/setores"

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
        

