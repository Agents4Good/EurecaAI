from .get_cursos import get_lista_cursos
from langchain_ollama import ChatOllama
from ..utils.most_similar import get_most_similar
from ..utils.processar_json import processar_json

model = ChatOllama(model="llama3.1", temperature=0)
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

    return processar_json(response.content, "curso")