from langchain_ollama import ChatOllama
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub
import warnings
warnings.filterwarnings("ignore", message="LangSmithMissingAPIKeyWarning")

class StateSQL(TypedDict):
    query: str
    question: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

class LLMGenerateSQL:
    def __init__(self, model: str, prompt: str):
        self.llm = ChatOllama(model=model, temperature=0)
        query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
        dict(query_prompt_template)['messages'][0].prompt.template = prompt
        self.query_prompt_template = query_prompt_template
  
    def write_query(self, query, tabela):
        prompt = self.query_prompt_template.invoke({
            'dialect': "sqlite",
            'table_info': tabela,
            'top_k': 10,
            'input': query
        })

        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}


tabela = """
CREATE TABLE IF NOT EXISTS Estudante (
    nome_do_estudante TEXT -- nome do estudante,
    matricula_do_estudante TEXT,
    turno_do_curso TEXT, -- ENUM que pode ser "Matutino", "Diurno", "Vespertino", "Noturno" ou "Integral".
    codigo_do_curriculo INTEGER, -- curriculo do aluno no curso.
    estado_civil TEXT, -- ENUM que pode ser "Solteiro" ou "Casado".
    sexo TEXT, -- ENUM que pode ser "MASCULINO" ou "FEMININO".
    forma_de_ingresso TEXT, -- ENUM que pode ser "SISU", "REOPCAO" OU "TRANSFERENCIA".
    nacionalidade TEXT, ENUM que pode ser "Brasileira" ou "Estrangeira".
    local_de_nascimento TEXT, -- Local (cidade) onde o estudante nasceu.
    naturalidade TEXT, -- Sigla do estado do estudante.
    cor TEXT, -- Enum que pode ser "Branca", "Preta", "Parda", "Indigena" ou "Amarela".
    deficiente TEXT, -- Enum que pode ser "Sim" ou "Não".
    ano_de_conclusao_ensino_medio INTEGER, 
    tipo_de_ensino_medio TEXT, -- ENUM que pode ser "Somente escola pública" ou "Somente escola privada". 
    cra REAL, -- Coeficiente de rendimento acadêmico.
    mc REAL, -- Média de conclusão de curso.
    iea REAL, --Indice de eficiência acadêmica.
    periodos_completados INTEGER, 
    prac_renda_per_capita_ate REAL
);
"""

prompt = '''
Essa tabela tem estudantes de um curso chamado "CIENCIA DA COMPUTAÇÃO - Diurno" do Campus de Campina Grande.
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - nome_do_estudante
  - matricula_do_estudante
  - turno_do_curso
  - codigo_do_curriculo
  - estado_civil
  - sexo
  - forma_de_ingresso
  - nacionalidade
  - local_de_nascimento
  - naturalidade
  - cor
  - deficiente
  - ano_de_conclusao_ensino_medio
  - tipo_de_ensino_medio
  - cra REAL
  - mc REAL
  - iea REAL
  - periodos_completados
  - prac_renda_per_capita_ate
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
'''


sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)


queries = [
    '''Qual é o CRA de Matheus Hensley?''',
    '''Quantos estrangeiros tem no curso?''',
    '''Quantos estudantes tem CRA acima da média?''',
    '''Quantos estudantes vieram do estado da paraiba?''',
    '''De onde vem os estudantes do curso por estado? Me mostre pra cada estado do país''',
    '''Quais são os 5 estudantes com maior cra do curso de ciência da computação do campus de campina grande?''',
    '''Quantos estudantes que estudam a noite no campus de campina grande?''',
    '''Existem quantos estudantes casados e solteiros no curso de engenharia de materiais do campus de campina grande?''',
    '''Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?'''
]

sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)

result = []
for query in queries:
    result.append((query, sqlGenerateLLM.write_query(query=query, tabela=tabela)))

for query, result in result:
    print(query)
    print(result)
    print()