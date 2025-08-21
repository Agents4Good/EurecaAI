from typing import Any
from utils.BASE_URL import BASE_URL
from mcp_server import mcp
import logging
from helpers.make_request import make_request
from utils.obter_info_func import get_func_info


@mcp.tool()
async def buscar_todos_estudantes_curso(campus: Any, curso: Any, situacao_estudante: Any = "", periodo_de_ingresso_de: Any = "", periodo_de_ingresso_ate: Any = "", periodo_de_evasao_de: Any = "", periodo_de_evasao_ate: Any = "") -> list[dict]:
    """
    Busca informações gerais dos estudantes da UFCG com base no(s) curso(s) e situação acadêmica.

    Args:
        campus (Any): código do campus.
        curso (Any): código do curso. 
        situacao_estudante (str): Situação do estudante. Valores permitidos:
            - 'SUSPENSOS'
            - 'REINGRESSOS'
            - 'REATIVADOS'
            - 'DESISTENTES'
            - 'EVADIDOS'
            - 'JUBILADOS'
            - 'ABANDONOS'
            - 'TRANSFERIDOS'
            - 'FINALIZADOS'
            - 'INATIVOS'
            - 'EGRESSOS'
            - 'ATIVOS'
        periodo_de_ingresso_de (Any, optional): Período inicial de ingresso. Defaults to "".
        periodo_de_ingresso_ate (Any, optional): Período final de ingresso. Defaults to "".
        periodo_de_evasao_de (Any, optional): Período inicial de evasão. Defaults to "".
        periodo_de_evasao_ate (Any, optional): Período final de evasão. Defaults to "".

    Returns:
        list[dict]: Lista de estudantes no formato:
            {
                "matricula_do_estudante": str,        # Matrícula do estudante
                "nome": str,                          # Nome completo
                "codigo_do_curso": int,               # Código do curso
                "nome_do_curso": str,                 # Nome do curso
                "turno_do_curso": str,                # Turno do curso (ex.: Matutino)
                "codigo_do_curriculo": int,           # Código do currículo
                "campus": int,                        # Código do campus
                "nome_do_campus": str,                # Nome do campus
                "codigo_do_setor": int,               # Código do setor responsável
                "nome_do_setor": str,                 # Nome do setor responsável
                "estado_civil": str,                  # Estado civil
                "endereco": str,                      # Endereço do estudante
                "sexo": str,                          # Sexo do estudante
                "data_de_nascimento": str,            # Data de nascimento
                "cpf": str,                           # CPF
                "cep": str,                           # CEP
                "telefone": str,                      # Telefone de contato
                "situacao": str,                      # Situação acadêmica do estudante
                "motivo_de_evasao": str,              # Motivo de evasão (se aplicável)
                "periodo_de_evasao": str,             # Período de evasão (se aplicável)
                "forma_de_ingresso": str,             # Forma de ingresso (ex.: SISU)
                "periodo_de_ingresso": str,           # Período de ingresso
                "email": str,                         # E-mail institucional
                "nacionalidade": str,                 # Nacionalidade
                "local_de_nascimento": str,           # Local de nascimento
                "naturalidade": str,                  # Naturalidade (UF)
                "cor": str,                           # Cor/raça
                "deficiencias": list[str],            # Lista de deficiências (se houver)
                "ano_de_conclusao_ensino_medio": int, # Ano de conclusão do ensino médio
                "tipo_de_ensino_medio": str,          # Tipo de ensino médio cursado
                "politica_afirmativa": str,           # Política afirmativa aplicada (ex.: L1)
                "cra": float,                         # Coeficiente de Rendimento Acadêmico
                "mc": float,                          # Média das notas
                "iech": float,                        # Índice de Eficiência em CH
                "iepl": float,                        # Índice de Eficiência por Período Letivo
                "iea": float,                         # Índice de Eficiência Acadêmica
                "mcn": float,                         # Média das Notas Normalizadas
                "iean": float,                        # Índice de Eficiência Acadêmica Normalizado
                "creditos_do_cra": int,               # Créditos válidos para cálculo do CRA
                "notas_acumuladas": float,            # Soma das notas acumuladas
                "periodos_completados": int,          # Quantidade de períodos concluídos
                "creditos_tentados": int,             # Créditos tentados
                "creditos_completados": int,          # Créditos completados
                "creditos_isentos": int,              # Créditos isentos
                "creditos_falhados": int,             # Créditos não aprovados
                "creditos_suspensos": int,            # Créditos suspensos
                "creditos_em_andamento": int,         # Créditos em andamento
                "velocidade_media": float,            # Velocidade média de integralização
                "taxa_de_sucesso": float,             # Taxa de sucesso acadêmico
                "prac_atualizado": str,               # Status de atualização PRAC
                "prac_atualizado_em": str,            # Data da última atualização PRAC
                "prac_cor": str,                      # Cor declarada na PRAC
                "prac_quilombola": str,               # Indica se é quilombola
                "prac_indigena_aldeado": str,         # Indica se é indígena aldeado
                "prac_renda_per_capita_ate": float,   # Renda per capita declarada
                "prac_deficiente": str,               # Indica se possui deficiência
                "prac_deficiencias": list[str],       # Lista de deficiências declaradas na PRAC
                "prac_deslocou_mudou": str,           # Se mudou de local por estudo
                "ufpb": int                           # Indica relação com UFPB (1 = sim)
            }
    """

    params = {
        "campus": campus,
        "curso": curso,
        "situacao-do-estudante": situacao_estudante,
        "periodo-de-ingresso-de": periodo_de_ingresso_de,
        "periodo-de-ingresso-ate": periodo_de_ingresso_ate,
        "periodo-de-evasao-de": periodo_de_evasao_de,
        "periodo-de-evasao-ate": periodo_de_evasao_ate
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/estudantes"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return f"Não foi possível obter os dados dos estudantes do curso {curso} do campus {campus}"
        
        return data
    except Exception as e:
        import traceback
        print(f"❌Tool {func_name} deu erro:", e)
        traceback.print_exc()
        raise



