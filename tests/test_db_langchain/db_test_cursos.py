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
CREATE TABLE IF NOT EXISTS Curso (
    codigo_do_curso INTEGER -- Codigo do curso (ID: chave primária)
    nome_do_curso Text, -- Nome do curso
    codigo_do_setor INTEGER, -- Código do setor ao qual o curso pertence
    nome_do_setor Text, -- Nome do setor ao qual o curso pertence
    nome_do_campus Text, -- ENUM que pode ser "Campina Grande", "Cajazeiras", "Sousa", "Patos", "Cuité", "Sumé" e "Pombal".
    turno Text, -- Turno do curso pode ser "Matutino", "Vespertino", "Noturno" e "Integral"
    periodo_de_inicio REAL, -- período em que o curso foi criado/fundado
    data_de_funcionamento Text, -- Data em formato de Texto sobre quando o curso foi criado "YYYY-MM-DD" (usar esses zeros), deve converter em date
    codigo_inep INTEGER, -- Código INEP do curso 
    modalidade_academica" Text, -- Pode ser "BACHARELADO" ou "LICENCIATURA"
    curriculo_atual INTEGER, -- É o ano em que a grade do curso foi renovada
    ciclo_enade INTEGER -- De quantos em quantos semestres ocorre a prova do enade 
);
"""

prompt = '''
Essa tabela tem cursos chamado "CIÊNCIA DA CUMPUTAÇÃO - D" localizado no campus da cidade de "Campina Grande".
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - codigo_do_curso
  - nome_do_curso
  - codigo_do_setor
  - nome_do_setor
  - campus
  - nome_do_campus
  - turno
  - periodo_de_inicio
  - data_de_funcionamento
  - codigo_inep
  - modalidade_academica
  - curriculo_atual
  - ciclo_enade
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
'''


sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)


queries = [
   '''Quais são os cursos de campina grande?''',
   '''Qual é o codigo do curso de ciencia da computação?''',
   '''Quero saber todos os nome e código dos cursos da UFCG''',
   '''Quando o enade irá ocorrer em ciencia da computação?''',
   '''Quando o curso de ciencia da computação foi criado?''',
   '''Quais são os cursos que ocorrem a noite e que sao bacharel?'''

]

sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)

result = []
for query in queries:
    result.append((query, sqlGenerateLLM.write_query(query=query, tabela=tabela)))

for query, result in result:
    print(query)
    print(result)
    print()