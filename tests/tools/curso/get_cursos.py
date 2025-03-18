import json
import requests
from typing import Any
from ..utils.base_url import URL_BASE
from ..campus.get_campi import get_campi
from ..campus.utils import get_campus_most_similar
from langchain_ollama import ChatOllama

prompt_sql_cursos = """
Você é um agente especialista em gerar comando SQL!

Curso (
    codigo_do_curso Number,
    descricao Text, // Nome do curso
    grau_do_curso Text, // Pode ser "LICENCIATURA" ou "BACHAREL"
    codigo_do_setor Number,
    nome_do_setor Text
    campus Number,
    nome_do_campus Text,
    turno Text, // Pode ser MATUTINO, VESPERTINO E NOTURNO
    periodo_de_inicio Double,
    data_de_funcionamento Text, // Date em formato de Texto
    codigo_inep Number,
    modalidade_academica" Text, // Pode ser "BACHARELADO" ou "LICENCIATURA"
    curriculo_atual Number,
    area_de_retencao Number,
    ciclo_enade Number
)

Gere apenas o comando SQL e mais nada!

Dado a tabela a acima, responda:
"{pergunta}"
"""

def get_cursos(pergunta_feita: Any, nome_do_campus: Any = "") -> list:
    """
    Busca por todos os cursos da UFCG por campus, apenas o código dele e o nome.

    Args:
    nome_do_campus: O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... E se quiser todos os cursos de todos os campus, passe a string vazia ''.

    Returns:
        Lista de cursos com 'codigo_do_curso' e 'descricao' que representa o nome e o turno do curso.
    """
    
    nome_do_campus=str(nome_do_campus)
    pergunta=str(pergunta)
    print(f"Tool get_cursos chamada com nome_do_campus={nome_do_campus}")
    
    params = {
        'status-enum':'ATIVOS',
    }

    if (nome_do_campus != ""):
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        params['campus'] = dados_campus["campus"]["codigo"]
    
    url_cursos = f'{URL_BASE}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)

        model = ChatOllama(model="llama3.1:8b", temperature=0)
        response = model.invoke(prompt_sql_cursos.format("Quantos cursos tem a UFCG?"))

        sql = response.content

        
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação dos cursos da UFCG."}]