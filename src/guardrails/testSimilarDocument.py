import sys
sys.path.append(r"D:\Workspace\python\agents4good\EurecaAI\src\guardrails")
from guardrails import Guard
from guardrails.hub import SimilarToDocument
from testSimilarityValidatorData import dados

def teste(eureca_output,llm_output):
    guard = Guard().use(
        SimilarToDocument,
        document=eureca_output,
        threshold=0.7,
        model="all-MiniLM-L6-v2",
        on_fail="exception",
    )
    try:
        guard.validate(llm_output)
    except Exception as e:
        print("Validação Falhou ", e)


for i in range(1,5):
    key_auxiliar = "test" + "_" + str(i);
    texto_eureca = dados[key_auxiliar]["response_eureca"]
    texto_llm = dados[key_auxiliar]["response_llm"]
    try:
        result = teste(texto_eureca, texto_llm)
    except Exception as e:
        print(f"Erro no teste {key_auxiliar}: {e}")

