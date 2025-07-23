from .utils import obter_disciplina_codigo
from .exception import NormalizeEstagioError

def normalize_data_estagio(data_json):
    """
        Normaliza os dados do estagio com o para incluir os campos que não existem nos dados.

        Adiciona os campos:
           - nome_do_setor: Nome do setor responsável pela disciplina estágio.
           - codigo_do_setor: Código do setor responsável pela disciplina estágio.
    """

    try:
        for item in data_json:
            campos_adicionais = {
                "nome_do_setor": "",
                "codigo_do_setor": ""
            }

            codigo_disciplina = item.get("codigo_da_disciplina")
            if codigo_disciplina:
                try:
                    disciplina = obter_disciplina_codigo(codigo_disciplina)
                    if disciplina and isinstance(disciplina, list):
                        campos_adicionais["nome_do_setor"] = disciplina[0].get("nome_do_setor", "")
                        campos_adicionais["codigo_do_setor"] = disciplina[0].get("codigo_do_setor", "")
                except Exception as e:
                    print(f"Erro ao obter disciplina para código {codigo_disciplina}: {e}")

            item.update(campos_adicionais)


        return data_json
    
    except Exception as e:
        raise NormalizeEstagioError(f"""Erro: Ocorreu um erro ao normalizar os dados. Causa: {str(e)}""")