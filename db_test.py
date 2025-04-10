from langchain_ollama import ChatOllama
from typing import TypedDict
from typing_extensions import Annotated
from langchain import hub

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
    nome_do_estudante TEXT, -- nome do estudante (nome de pessoa).
    matricula_do_estudante TEXT, -- Número de 9 digitos que representa o número da matrícula do estudante (usar se informou a matrícula do estudante).
    status TEXT, -- É um ENUM que representa a situação do estudante na disciplina. O ENUM pode ser "Aprovado", "Trancado", "Reprovado por Nota", "Reprovado por Falta". E quando peguntar apenas uma palavra próximo a reprovação sem especificar se foi por nota ou por falta use "Reprovado por Nota" OR Reprovado por Falta".
    media_final REAL, -- Nota do aluno na disciplina (usar se pedir informações de notas e médias).
    dispensou TEXT -- ENUM que pode ser "Sim" ou "Não". (usar se perguntar sobre dispensas).
);
"""

prompt = '''
Essa tabela tem estudantes de uma disciplina chamada "TEORIA DA COMPUTAÇÃO - D" do cuso de "CIENCIA DA COMPUTAÇÃO - INTEGRAL".
Dada uma pergunta de entrada, crie uma consulta ({dialect}) sintaticamente correta para executar e ajudar a encontrar a resposta.

Use apenas a seguintes tabela a seguir:

{table_info}

Siga **rigorosamente** as instruções abaixo:

<RESTRIÇÕES>
- Nunca use "SELECT *" — selecione somente as colunas relevantes.
- Utilize **apenas os nomes de colunas exatamente como descritos** no esquema:
  - nome_do_estudante
  - matricula_do_estudante
  - status
  - media_final
  - dispensou
- Não invente ou modifique os nomes das colunas.
- Nunca use a cláusula LIKE.
- Ignore referências a "turma" pois não há nenhuma coluna representando isso.
- Se uma parte da pergunta não se relaciona com o esquema, ignore.
</RESTRIÇÕES>

Responda com uma consulta SQL válida e mínima.
'''


sqlGenerateLLM = LLMGenerateSQL(model="llama3.1", prompt=prompt)


queries = [
    '''Quero o nome do estudante que tem a maior nota na turma 1 de ciencia da computação?''',
    '''Qual é a quantidade de estudantes na turma 1 de Teoria da Computação em ciencia da computação?''',
    '''Sobre a disciplina de teroria da computação, quantos estudantes existem na turma 1?''',
    '''Qual foi a nota de Matheus Hensley de Figueiredo e Silva na disciplina de teoria da computação?''',
    '''Qual é o nome e a matricula dos 8 estudantes que tiraram a maior nota em Teoria da Computação do curso de Ciência da Computação?''',
    '''Qual foi a média das média das notas dos estudantes da disciplina de Teoria da Computação do curso de ciência da computação?''',
    '''Qual foi a media de Joao e Pedro na disciplina de Teoria da Computação do curso de ciencia da computação?''',
    '''Quais foram os estudantes que passaram na disciplina de Teoria da computação do curso de ciencia da computacao''',
    '''Quais foram os estudantes que reprovaram a disciplina de Teoria da computação do curso de ciencia da computação''',
    '''Quantos foram os estudantes que reprovaram por falta a disciplina de Teoria da computação do curso de ciencia da computação''',
    '''Quais foram os estudantes que reprovaram por nota a disciplina de Teoria da computação do curso de ciencia da computação''',
    '''Quais forão os estudantes que dispensaram a disciplina?''',
    '''Qual foi a menor nota dos alunos na disciplina?''',
    '''Quantos alunos tiraram nota entre 5 e 7?''',
    '''Qual é o percentual dos alunos aprovados e reprovados na disciplina?''',
    '''Qual é o percentual dos alunos reprovados na disciplina?''',
    '''Qual foi o aluno que tirou nota 9.2 na disciplina?''',
    '''Qual foi o safado que tirou 10 na disciplina?''',
    '''Qual é a matricula de todos os estudantes da disciplina?'''
]

for query in queries:
    print(sqlGenerateLLM.write_query(query=query, tabela=tabela))