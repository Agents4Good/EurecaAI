import sys
#sys.path.append(r"D:\Workspace\python\agents4good\EurecaAI\src\guardrails")
sys.path.append(r"/home/levi/Agents4Good/EurecaAI")
from guardrails import Guard
from guardrails.hub import SimilarToDocument
from .testSimilarityValidatorData import dados

def teste(eureca_output,llm_output):
    res = guard = Guard().use(
        SimilarToDocument,
        document=eureca_output,
        threshold=0.7,
        model="all-MiniLM-L6-v2",
        on_fail="exception",
    )
    
    #print("RES ", res)
    #print(type(res))
    #print(dir(res))
    try:
        return guard.validate(llm_output)
    except Exception as e:
        print("Validação Falhou ", e)
        return e


for i in range(1,5):
    key_auxiliar = "test" + "_" + str(i);
    texto_eureca = dados[key_auxiliar]["response_eureca"]
    texto_llm = dados[key_auxiliar]["response_llm"]
    try:
        result = teste(texto_eureca, texto_llm)
        print("RES-------------------------------------------------------------------", result)
        print(type(result))
        print(dir(result))
    except Exception as e:
        print(f"Erro no teste {key_auxiliar}: {e}")

