
from guardrails.validators import (register_validator, Validator, FailResult, ValidationResult, PassResult)
from guardrails import Guard
from typing import Any, Dict, Optional, Callable
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
import datetime as dt

"""
Esta classe é um Guardrail que camufla a matricula do estudante presente no texto passado como parâmetro.
"""
@register_validator(name="guardrails/enrollment", data_type="string")
class PIIValidatorEnrollment(Validator):
    def __init__(self, on_match: Optional[str] = None, on_fail: Optional[Callable] = None):
        super().__init__(on_match=on_match, on_fail=on_fail)
        
    
    def validate(self, value: str, metadata: Dict = {}) -> ValidationResult:
        year = str(dt.datetime.now().year)[2:]
        
        enrollment = r"\b\d{1}[1-" + year[0] + r"]" + r"[0-" + year[1] + r"]" + r"[12]\d{5}\b"
        enrollment_pattern = Pattern(name="Enrollment_Pattern", regex=enrollment, score=0.6)
        
        enrollment_recognizer = PatternRecognizer(name="MATRICULA", patterns=[enrollment_pattern], supported_entity="Enrollment_Pattern", supported_language="en")
        
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(enrollment_recognizer)
        
        results = analyzer.analyze(text=value, entities=["Enrollment_Pattern"], language="en")
        
        if results:
            for result in results:
                start, end = result.start, result.end
                value = value[:start] + "<MATRICULA>" + value[end:]
            return FailResult(error_message=value)
        
        return PassResult()


"""
Esta classe é um Guardrail que camufla a o CPF presente no texto passado como parâmetro.
"""
@register_validator(name="guardrails/cpf", data_type="string")
class PIIValidatorCPF(Validator):
    def __init__(self, on_match: Optional[str] = None, on_fail: Optional[Callable] = None):
        super().__init__(on_match=on_match, on_fail=on_fail)
        
        
    def validate_digit_verificator(self, cpf):
        
        soma = 0
        for i in range(1, len(cpf) + 1):
            soma += i * int(cpf[i - 1])
            
        primeiro_digito_verificador = soma % 11
        
        if primeiro_digito_verificador == 10:
            primeiro_digito_verificador = 0
        
        soma = 0
        cpf = cpf + primeiro_digito_verificador
        for i in range(len(cpf)):
            soma += i * int(cpf[i])
        
        segundo_digito_verificador = soma % 11
        
        if segundo_digito_verificador == 10:
            segundo_digito_verificador = 0
        
        cpf_ = cpf[-2:]
        return cpf_ == cpf[-2:]
        
        
    def validate(self, value: str, metadata: Dict = {}) -> ValidationResult:
        year = str(dt.datetime.now().year)[2:]
        
        cpf_regex = r"\b\d{3}\.*\d{3}\.*\d{3}-*\d{2}\b"
        cpf_pattern = Pattern(name="CPF_Pattern", regex=cpf_regex, score=0.6)
        
        cpf_recognizer = PatternRecognizer(name="MATRICULA", patterns=[cpf_pattern], supported_entity="CPF_Pattern", supported_language="en")
        
        analyzer = AnalyzerEngine()
        analyzer.registry.add_recognizer(cpf_recognizer)
        
        results = analyzer.analyze(text=value, entities=["CPF_Pattern"], language="en")
        
        if results:
            for result in results:
                start, end = result.start, result.end
                value = value[:start] + "<CPF>" + value[end:]
            return FailResult(error_message=value)
        
        return PassResult()