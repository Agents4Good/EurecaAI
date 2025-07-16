from .get_professores_setor import get_professores_setor
from ..campus.utils import get_campus_most_similar
from ..disciplina.get_disciplinas import get_disciplinas
from ..campus.utils import get_campus_most_similar
from ...sql.GerenciadorSQLAutomatizado import GerenciadorSQLAutomatizado
from ...sql.Estagio.normalize_data import normalize_data_estagio
from ...sql.Estagio.prompt import PROMPT_SQL_ESTAGIO
from ..utils.base_url import URL_BASE
from ..utils.remover_parametros_query import remover_parametros_da_query
from datetime import datetime
from typing import Any
import requests
import json
import unicodedata

def get_estagios(query: Any, ano_de: Any = "", ano_ate: Any = "", nome_do_campus: Any = "", nome_do_centro_unidade: Any = "", nome_do_curso: Any = "") -> list:
    """
    __summary__
    Recupera informações sobre estágios da UFCG com base nos filtros fornecidos.
    Essa ferramenta retorna:
    - ID do estágio
    - Matrícula do estudante
    - Matrícula do professor orientador
    - ID da empresa
    - Data de início e fim do estágio
    - Carga horária
    - Valor da bolsa
    - Auxílio transporte
    - Nome do setor e código do setor

    📅 INSTRUÇÕES SOBRE PARÂMETROS DE ANO:
    - Se o usuário disser "desde [ANO]" (ex: "desde 2020"), então preencha apenas `ano_de` com esse ano (ex: `ano_de=2020`).
    - Se o usuário disser "até [ANO]", preencha apenas `ano_ate` com esse ano.
    - Se o usuário disser "em [ANO]" ou informar apenas um ano sem contexto de início/fim, preencha `ano_de` e `ano_ate` com o mesmo ano.
    - Se nenhuma data for mencionada, deixe ambos (`ano_de` e `ano_ate`) como string vazia.

    🏫 FILTROS ADICIONAIS:
    - `nome_do_campus`: cidade onde fica o campus (ex: "Campina Grande", "Cajazeiras", ...). Se quiser dados de todos os campi, passe string vazia "".
    - `nome_do_centro_unidade`: nome completo do centro, unidade ou curso (ex: "Unidade Acadêmica de Engenharia Elétrica"). Para dados de toda a UFCG, passe "".
    - `nome_do_curso`: nome exato do curso, se desejar filtrar por curso específico.

    Args:
        query (Any): A pergunta original feita pelo usuário.
        ano_de (Any): Ano de início (ex: 2020). Ver instruções acima.
        ano_ate (Any): Ano de término (ex: 2023). Ver instruções acima.
        nome_do_campus (Any): Nome do campus da UFCG.
        nome_do_centro_unidade (Any): Nome da unidade acadêmica ou centro.
        nome_do_curso (Any): Nome do curso.

    Returns:
        list: Lista de registros de estágios contendo os campos descritos acima.
    
    """

    
    #query = str(query)
    query = remover_parametros_da_query(query, excluir=['self'])
    print(f"Query com os termos removidos: {query}")


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
    
    if len(estagios_filtrados) == 0:
        return "Erro: Informe para passar os dados necessarios nessa ferramenta"
    

    estagios_filtrados_normalizados = normalize_data_estagio(estagios_filtrados)
    gerenciador = GerenciadorSQLAutomatizado(table_name="Estagio", db_name="db_estagio.sqlite", prompt= PROMPT_SQL_ESTAGIO)

    gerenciador.save_data(estagios_filtrados_normalizados)
    return gerenciador.get_data('estagio', query, True)


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
            #EXISTEM ALGUNS CÓDIGOS QUE SÃO NONE
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
