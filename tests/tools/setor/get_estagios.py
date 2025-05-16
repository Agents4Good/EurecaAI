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

def get_estagios(query: Any, ano_de: Any = "", ano_ate: Any = "", nome_do_campus: Any = "", nome_do_centro_unidade: Any = "", nome_do_curso: Any = "") -> list:
    """
    Buscar informações sobre estágios dos estudantes de uma centro da unidade de um curso.
    Se for informado apenas um ano, usar o mesmo ano no parâmetrio ano_de e ano_ate.
    Se for informado apenas um ano e você identificar que é a data de ínicio, mas que não é a de término, então só passe o ano apenas em ano_de.
    Se for informado apenas um ano e você identificar que é a data limite, mas que não é de início, então so passe o ano apenas em ano_ate.

    Args:
        query (Any): Pergunta do usuário.
        ano_de (Any): ano em valor inteiro de início dos estágios (use o ano perguntado, se não souber use vazio ""). Defaults to "". 
        ano_ate (Any): ano em valor inteiro do ano limite para busca (use o ano perguntado, se não souber use vazio ""). Defaults to "". 
        nome_do_campus (Any): O parâmetro nome do campus é nome da cidade onde reside o campus e ela pode ser uma dessas a seguir: Campina Grande, Cajazeiras, Sousa, Patos, Cuité, Sumé, Pombal, ... (se não foi informado ou se quiser saber sobre todos os centros, então passe a string vazia '').
        nome_do_centro_unidade (Any): nome do setor (nome do centro, nome da unidade ou nome do curso) do curso, e passe a informação completa como "centro de ..." ou "unidade academica de ...". (Caso queira de toda a UFCG passe o parâmetro com string vazia '').
        nome_do_curso (Any): Nome do curso.
    
    Returns:
        Lista com informações relevantes de estágio.
    """
    
    query = str(query)
    nome_do_campus=str(nome_do_campus)
    nome_do_curso=str(nome_do_curso)
    nome_do_centro_unidade=str(nome_do_centro_unidade)
    ano_de=str(ano_de)
    ano_ate=str(ano_ate)
    if ano_ate == "":
        ano_ate = str(datetime.now().year)
    
    print(f"Tool get_estagios chamada com nome_do_campus={nome_do_campus}, nome_do_centro_unidade={nome_do_centro_unidade}, nome_do_curso={nome_do_curso}, ano_de={ano_de} e ano_ate={ano_ate}")
    params = {
        "inicio-de": ano_de,
        "fim-ate": ano_ate
    }

    response = requests.get(f'{URL_BASE}/estagios', params=params)

    if response.status_code != 200:
        return [{"error_status": response.status_code, "msg": "Não foi possível obter informação da UFCG."}]
    
    estagios = json.loads(response.text)
    estagios_filtrados = filtragem(nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, nome_do_centro_unidade=nome_do_centro_unidade, estagios=estagios)
    
    print("Okay")
    if len(estagios_filtrados) == 0:
        return "Erro: Informe para passar os dados necessarios nessa ferramenta"
    print("Okay2")

    estagios_filtrados_normalizados = normalize_data_estagio(estagios_filtrados)
    gerenciador = GerenciadorSQLAutomatizado(table_name="Estagio", db_name="db_estagio.sqlite")
    gerenciador.save_data(estagios_filtrados_normalizados)
    return gerenciador.get_data(query, PROMPT_SQL_ESTAGIO, temperature=0)


#FUNÇÂO AUXILIAR
def filtragem(nome_do_campus, nome_do_curso, nome_do_centro_unidade, estagios):
    estagios_filtrados = []

    if not nome_do_campus and not nome_do_curso and not nome_do_centro_unidade:
        return estagios
    
    elif nome_do_campus and not nome_do_curso and not nome_do_centro_unidade:
        print("primeira condição")
        dados_campus = get_campus_most_similar(nome_do_campus=nome_do_campus)
        codigo_campus = str(dados_campus["campus"]["codigo"])

        for estagio in estagios:
            codigo = estagio["codigo_da_disciplina"]
            #EXISTEM ALGUNS CÒDIGOS QUE SÂO NONE
            if codigo is not None and str(codigo)[0] == codigo_campus:
                estagios_filtrados.append(estagio)
    
    elif nome_do_campus and nome_do_centro_unidade:
        print("segunda condição")
        professores = get_professores_setor(nome_do_campus=nome_do_campus, nome_do_centro_setor=nome_do_centro_unidade)
        codigo_professores = [professor["matricula_do_docente"] for professor in professores]
        for estagio in estagios:
            if estagio["matricula_do_docente"] in codigo_professores:
                estagios_filtrados.append(estagio)
    
    elif nome_do_campus and nome_do_curso:
        print("terceira condição")
        disciplinas = get_disciplinas(query="", nome_do_campus=nome_do_campus, nome_do_curso=nome_do_curso, curriculo=" ") #CURRICULO TEM QUE PASSAR UM ESPAÇO EM BRANCO

        disciplinas_de_estagios = [
                disciplina["codigo_da_disciplina"]
                for disciplina in disciplinas
                if "estagio" in unicodedata.normalize("NFKD", disciplina["nome"]).encode("ASCII", "ignore").decode("utf-8").lower()
        ]

        for estagio in estagios:
            if estagio["codigo_da_disciplina"] in disciplinas_de_estagios:
                estagios_filtrados.append(estagio)

    return estagios_filtrados
