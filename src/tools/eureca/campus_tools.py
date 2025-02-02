import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strawberry_demo.main import schema
from langchain_core.tools import tool
from .default_data.default_campus_data import *


@tool
def get_campi(data: str = default_campus):
        """
        Buscar todos os campi.
        """
        try:
            query = f"""
                    query {{allCampus     
                    {{ 
                        {data} 
                    }}
                }}
            """
            print(f"Tool get campi chamada com args {data}")
            result = schema.execute_sync(query)
            return result.data['allCampus']
        except Exception as e:
            return e

@tool
def get_calendarios(data: str = default_calendario):
    """
    Buscar calendários da universidade do campus 1 da UFCG. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    """
    try:
        query = f"""
                    query {{calendarios
                        {{
                            {data}
                        }}
                    }}
                """
        print(f"Tool get calendarios chamada com args {data}")

        result = schema.execute_sync(query)
        
        return result.data['calendarios']
    except Exception as e:
            return e

@tool
def get_periodo_mais_recente(data: str = default_calendario):
    """
    Buscar o período mais recente da universidade.
    """
    try:
        query = f"""
                    query {{periodoMaisRecente
                        {{
                            {data}
                        }}
                    }}
                """
        print(f"Tool get periodo mais recentee chamada com args {data}")

        result = schema.execute_sync(query)
        return result.data['periodoMaisRecente']
    except Exception as e:
            return e
   

#DOCUMENTAÇÂO DAS FUNÇÕES
get_campi.__doc__ = f"""
        Args:
            data: campos a serem retornados, por padrão é {default_campus}
    
        Returns:
            Lista com dicionários que possuem os campos desejados. Por padrão é
            {default_campus}.
"""

get_calendarios.__doc__ = f""" 
    Args:
        data: campos a serem retornados, por padrão é {default_calendario}

    Returns:
       Lista com dicionários que possuem os campos desejados. Por padrão é{default_calendario}
"""

get_periodo_mais_recente.__doc__ = f""" 
    Args:
        data: campos a serem retornados, por padrão é {default_calendario}

    Returns:
       Lista com dicionários que possuem os campos desejados. Por padrão é{default_calendario}
"""



