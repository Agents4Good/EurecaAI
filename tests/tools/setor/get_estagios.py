from .get_professores_setor import get_professores_setor
from ..campus.utils import get_campus_most_similar
from ..disciplina.get_disciplinas import get_disciplinas
from ..campus.utils import get_campus_most_similar

from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ...sql.Estagio.normalize_data import normalize_data_estagio
from ...sql.Estagio.prompt import PROMPT_SQL_ESTAGIO

from ..utils.base_url import URL_BASE
from datetime import datetime
from typing import Any
import requests
import json
import unicodedata

def get_estagios(ano: Any, query: Any,  nome_do_campus: Any = "", nome_do_centro_unidade: Any = "", nome_do_curso: Any = "") -> list:
    """
    Buscar informações sobre estágios dos estudantes de uma centro da unidade de um curso.

    Args:
        ano (Any): ano (use o ano perguntado).
        query (Any): Pergunta do usuário.
        nome_do_campus (Any): O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (se não foi informado ou se quiser saber sobre todos os centros, então passe a string vazia '').
        nome_do_centro_unidade (Any): nome do setor (nome do centro, nome da unidade ou nome do curso) do curso, e passe a informação completa como "centro de ..." ou "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        nome_do_curso (Any): Nome do curso.
    
    Returns:
        Lista com informações relevantes de estágio.
    """
    
    query = str(query)
    nome_do_campus=str(nome_do_campus)
    nome_do_centro_unidade=str(nome_do_centro_unidade)
    ano=str(ano)
    if ano == "":
        ano = str(datetime.now().year)
    
    print(f"Tool get_estagios chamada com nome_do_campus={nome_do_campus}, nome_do_centro_unidade={nome_do_centro_unidade} e ano={ano}")
    params = {
        "inicio-de": str(ano),
        "fim-ate": str(ano)
    }


    response = requests.get(f'{URL_BASE}/estagios', params=params)
    if response.status_code != 200:
        return "Erro: "
    
    estagiarios = json.loads(response.text)
    estagiarios_filtrados = []
    
    if nome_do_campus and not nome_do_curso and not nome_do_centro_unidade:
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        codigo_campus = str(dados_campus["campus"]["codigo"])
        for estagiario in estagiarios:
            if estagiario["codigo_disciplina"][0] == codigo_campus:
                estagiarios_filtrados.append(estagiario)
    
    elif nome_do_campus and nome_do_centro_unidade:
        professores = get_professores_setor(nome_do_campus=nome_do_campus, nome_do_centro_setor=nome_do_centro_unidade)
        codigo_professores = [professor["matricula_do_docente"] for professor in professores]
        for estagiario in estagiarios:
            if estagiario["matricula_do_docente"] in codigo_professores:
                estagiarios_filtrados.append(estagiario)
    
    elif nome_do_campus and nome_do_curso:
        disciplinas = get_disciplinas(query="", nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo="")
        disciplinas_de_estagios = [disciplina["codigo_da_disciplina"] for disciplina in disciplinas if "estagio" in disciplina["nome"].apply(lambda x: unicodedata.normalize("NFKD", x).encode("ASCII", "ignore").decode("utf-8").lower())]
        for estagiario in estagiarios:
            if estagiario["codigo_disciplina"] in disciplinas_de_estagios:
                estagiarios_filtrados.append(estagiario)
    
    else:
        return "Erro: Informe para passar os dados necessarios nessa ferramenta"

    estagiarios_filtrados = normalize_data_estagio(estagiarios_filtrados)
    if estagiarios_filtrados:
        gerenciador = GerenciadorSQLAutomatizado(table_name="Estagio", db_name="db_estagio.sqlite")
        gerenciador.save_data(estagiarios_filtrados)
        return gerenciador.get_data(query, PROMPT_SQL_ESTAGIO, temperature=0)
    else:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]