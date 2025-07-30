from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request

@mcp.tool()
async def buscar_todas_disciplinas_curso(campus: Any = 1, curso: Any = 14102100) -> str | list[dict]:
    """
    Busca todas as disciplinas de um curso de um determinado campus

    Args:
        campus: código do campus. Default = 1.
        curso: código do curso. Default = 14102100.
    
    Returns:
        Resposta da tool
    """

    params = {
        "status": 'ATIVOS',
        "campus": campus, 
        "curso": curso
    }

    try:

        logging.info(f"Chamando a API com campus={campus}, curso={curso}")
        url = f"{BASE_URL}/disciplinas"
        data = await make_request(url, params)


        if not data:
            return "Não foi possível obter as disciplinas ou nenhuma disciplina foi encontrada"
        
        print("Resultado da chamada:", data[0:10])
        return data[0:10]
    except Exception as e:
        import traceback
        print("❌ Tool deu erro:", e)
        traceback.print_exc()
        raise  # Se você quiser que o erro continue subindo (bom pra debug)
        



# import asyncio

# async def main():
#     resultado = await buscar_todas_disciplinas_curso(campus=1, curso=14102100)
#     print("Resultado da chamada:", resultado)

# if __name__ == "__main__":
#     asyncio.run(main())
