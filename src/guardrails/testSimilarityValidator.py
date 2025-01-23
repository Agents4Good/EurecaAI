import sys
sys.path.append(r"D:\Workspace\python\agents4good\EurecaAI\src\guardrails")
from guardrails import Guard
from src.guardrails.similarity_validator import SimilarityValidator
from testSimilarityValidatorData import dados

from guardrails.validators import (register_validator, Validator, FailResult, ValidationResult, PassResult)

def teste(eureca_output, llm_output):
    guard = Guard().use(
        SimilarityValidator(texto1=eureca_output, texto2=llm_output)      
    )
    try:
        guard.parse("Agente Inteligente").model_validate
    except  Exception as e:
        print(e)

   
for i in range(1,5):
    key_auxiliar = "test" + "_" + str(i);
    texto_eureca = dados[key_auxiliar]["response_eureca"]
    texto_llm = dados[key_auxiliar]["response_llm"]
    try:
        result = teste(texto_eureca, texto_llm)
    except Exception as e:
        print(f"Erro no teste {key_auxiliar}: {e}")


