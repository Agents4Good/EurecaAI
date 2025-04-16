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
    nome_do_estudante TEXT, -- Nome completo do estudante.
    matricula_do_estudante TEXT, -- Número de matrícula do estudante (exatamente 9 dígitos). Esse é o atributo da chave primária.
    turno_do_curso TEXT, -- Período do dia em que o curso é realizado. ENUM de possíveis valores: "Matutino", "Diurno", "Vespertino", "Noturno", "Integral".
    codigo_do_curriculo INTEGER, -- Ano de atualização da grade curricular do curso seguido do período. Por exemplo 2010.2 (ano de 2010 e segundo período).
    estado_civil TEXT, -- Estado civil do estudante. ENUM  de possíveis valores: "Solteiro" ou "Casado".
    sexo TEXT, -- Sexo biológico. ENUM de possíveis valores: "MASCULINO" ou "FEMININO".
    forma_de_ingresso TEXT, -- Forma de entrada na universidade. ENUM de possíveis valores: "SISU", "REOPCAO", "TRANSFERENCIA". (usar se)
    nacionalidade TEXT, -- Nacionalidade do estudante. ENUM de possíveis valores: "Brasileira" ou "Estrangeira"
    local_de_nascimento TEXT, -- Cidade onde o estudante nasceu. Exemplo: "Campina Grande"
    naturalidade TEXT, -- Estado (UF) do estudante. Exemplo: "PB", "PE"
    cor TEXT, -- Cor da pele. ENUM de possíveis valores: "Branca", "Preta", "Parda", "Indigena", "Amarela"
    deficiente TEXT, -- Se o estudante possui alguma deficiência. ENUM de possíveis valores: "Sim" ou "Não"
    ano_de_conclusao_ensino_medio INTEGER, -- Ano em que terminou o ensino médio. Exemplo: 2019
    tipo_de_ensino_medio TEXT, -- Tipo de escola em que estudou no ensino médio. ENUM de possíveis valores: "Somente escola pública", "Somente escola privada"
    cra REAL, -- Coeficiente de rendimento acadêmico do estudante / aluno. Exemplo: 7.45
    mc REAL, -- Média de conclusão do curso do estudante / aluno. Exemplo: 8.1
    iea REAL, -- Índice de eficiência acadêmica do estudante / aluno. Exemplo: 9.0
    periodos_completados INTEGER, -- Quantidade de períodos cursados pelo estudante. Exemplo: 6
    prac_renda_per_capita_ate REAL -- Renda média mensal da família (per capita). Exemplo: 645.32. Observação: Um salário mínimo é R$1528.00
);
"""

prompt = """
Essa tabela tem estudantes de uma disciplina chamada "TEORIA DA COMPUTAÇÃO - D" do cuso de "CIENCIA DA COMPUTAÇÃO - INTEGRAL".
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕESS>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
    nome_do_estudante
    matricula_do_estudante
    turno_do_curso
    codigo_do_curriculo
    estado_civil
    sexo
    forma_de_ingresso
    nacionalidade
    local_de_nascimento
    naturalidade
    cor
    deficiente
    ano_de_conclusao_ensino_medio
    tipo_de_ensino_medio
    cra
    mc
    iea
    periodos_completados
    prac_renda_per_capita_ate
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Sua saída deve ser **apenas uma consulta SQL válida e mínima**, sem comentários nem explicações.
Use apenas os atributos que forem pedidos na pergunta.
"""


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
    '''Quantos estudantes homens tem cra acima de 8 no curso de ciencia da computacao no campus de campina grande?''',
    '''Quem são os estudantes que estão no 5 período do curso?''',
    '''Quem sao os estudantes que transferiram de curso que são da cidade de caturite?''',
    '''Quem são os alunos de escola pública que estudam no curso de ciencia da computacao que vieram da cidade de aroeiras''',
    '''qual é o índice de eficiência acadêmica de caique?''',
    '''quantos estudantes sao pardos e indigenas no curso de ciencia da computacao do campus de campina grande?''',
    '''quantas pessoas tem renda entre 1 a 10 salario minimo?'''
]

sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)

result = []
for query in queries:
    result.append((query, sqlGenerateLLM.write_query(query=query, tabela=tabela)))

for query, result in result:
    print(query)
    print(result)
    print()