
from .utils import obter_disciplina_codigo

def normalize_data_estagio(data_json):
    """
        Normaliza os dados do estagio com o para incluir os campos que não existem nos dados.

        Adiciona os campos:
           - nome_do_setor: Nome do setor responsável pela disciplina estágio.
           - codigo_do_setor: Código do setor responsável pela disciplina estágio.
    """

    for item in data_json:
        campos_adicionais = {
            "nome_do_setor": "",
            "codigo_do_setor": ""
        }

       
        #ALGUNS ESTAGIOS TEM CODIGO DA DISCIPLINA COMO NONE  ELES FICAM COM NOME DO SETOR E CODIGO DO SETOR COMO VAZIO
        if item["codigo_da_disciplina"] is not None:
            disciplina = obter_disciplina_codigo(item["codigo_da_disciplina"])
            campos_adicionais["nome_do_setor"] = disciplina[0]["nome_do_setor"]
            campos_adicionais["codigo_do_setor"] = disciplina[0]["codigo_do_setor"]


        for campo, valor in campos_adicionais.items():
            item[campo] = valor

    return data_json