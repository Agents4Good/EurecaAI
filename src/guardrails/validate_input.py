from guardrails import Guard

from src.guardrails.cpf_validator import CPFValidator
from src.guardrails.matricula_validator import MatriculaValidator
from guardrails.hub import DetectPII

def validate(text):
    """
        função genérica que valida se o texto fornecido apresenta CPF, MATRÍCULA, EMAIL, NÚMERO DE TELEFONE
    """
    guard = Guard().use_many(CPFValidator)

    try:
        result = guard.parse(text)
    except Exception as e:
        text = str(e)[41:]
    
    guard = Guard().use(MatriculaValidator)

    try:
        result = guard.parse(text)
    except Exception as e:
        text = str(e)[41:]

    guard = Guard().use(DetectPII(pii_entities="pii", on_fail="fix"))

    result = guard.parse(llm_output=text, metadata={"pii_entities": ["EMAIL_ADDRESS", "URL", "PHONE_NUMBER"]})
    return result.validated_output