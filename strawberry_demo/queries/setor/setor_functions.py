from .default_data import *
from strawberry_demo.main import schema

def get_setores(data: str = default_setor):
    try:
        query = f"""query{{
                    setores {{
                        {data}
                    }}
                }}"""
        
        print(f"Tool get_setores com data {data}")
        result = schema.execute_sync(query);
        return result.data["setores"]
    except Exception as e:
        return e


def get_professores(codigo_do_setor: str, data: str = default_professor):
    try:
        query = f"""query{{
                    professores(codigoDoSetor: "{codigo_do_setor}") {{
                        {data}
                    }}
                }}"""
        
        variables = {
            "codigoDoSetor": codigo_do_setor
        }
        print(f"Tool get_professoes setor {codigo_do_setor} e data {data}")
        result = schema.execute_sync(query, variable_values=variables);
        return result.data["professores"]
    except Exception as e:
        return e
    
def get_total_professores(codigo_do_setor: str, data: str = default_professor):
    try:
        query = f"""query{{
                    professores(setorCentro: "{codigo_do_setor}") {{
                        {data}
                    }}
                }}"""
        
        variables = {
            "codigoDoSetor": codigo_do_setor
        }
        print(f"Tool get__total_professoes setor {codigo_do_setor} e data {data}")
        result = schema.execute_sync(query, variable_values=variables);
        return result.data["professores"]
    except Exception as e:
        return e
    
    


