import json
import requests
from langchain_ollama import ChatOllama
from ..utils.most_similar import get_most_similar
from ..utils.processar_json import processar_json
from ..campus.utils import get_campus_most_similar
from ..utils.base_url import URL_BASE
from langchain_community.chat_models import ChatDeepInfra



model = ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0)
#model = ChatOllama(model="llama3.1", temperature=0)
mapper_curso = {"nome": "descricao", "codigo": "codigo_do_curso"}
format = """{'curso': {'codigo': '', 'nome': ''}}"""

def get_curso_most_similar(nome_do_curso: str, nome_do_campus: str) -> dict:
    """
    Busca o nome e o código do curso pelo nome dele.

    Args:
        nome_do_curso: nome do curso.
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        dict: dicionário contendo código do curso e nome do curso.
    """
    
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    cursos = get_lista_cursos(nome_do_campus=nome_do_campus)
    cursos_most_similar, top_k = get_most_similar(lista_a_comparar=cursos, dado_comparado=nome_do_curso, top_k=5, mapper=mapper_curso, limiar=0.5)
    
    if len(cursos_most_similar) == 0:
        return {"AskHuman": "Não foi encontrado um curso com o nome o informado", "choice": top_k}

    response = model.invoke(
        f"""
        Para o curso de nome: '{nome_do_curso}', quais desses possíveis cursos abaixo é mais similar ao curso do nome informado?
        
        {cursos_most_similar}
        
        Responda no seguinte formato:
        
        {format}
        
        Não adicione mais nada, apenas a resposta nesse formato (codigo e nome).
        
        Antes de responder por definitivo, considere essas observações abaixo:

        M significa que é um curso matutino;
        D significa que é um curso diurno;
        N significa que é um curso noturno.
        """
    )
    resultado = processar_json(response.content, "curso")
    print(f"curso mais similar: {resultado}")
    return resultado


def get_lista_cursos(nome_do_campus: str) -> list:
    """
    Função auxiliar que busca todos os cursos do campus informado.

    Args:
        nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ...

    Returns:
        list: lista de cursos.
    """

    print("get_lista_cursos sendo usada.")
    params = { 'status': 'ATIVOS', 'campus': "" }
    url_cursos = f'{URL_BASE}/cursos'

    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]
    
    response = requests.get(url_cursos, params=params)

    cursos = []
    if response.status_code == 200:
        resposta_cursos = json.loads(response.text)
        for curso in resposta_cursos:
            nome_curso = curso["descricao"]
            codigo_curso = curso["codigo_do_curso"]
            cursos.append({"codigo_do_curso": codigo_curso, "descricao": nome_curso})
        return cursos
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]