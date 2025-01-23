
from guardrails.validators import (register_validator, Validator, FailResult, ValidationResult, PassResult)
from guardrails import Guard
from typing import Any, Dict, Optional, Callable
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, RecognizerResult, Pattern
import datetime as dt
import re

@register_validator(name="guardrails/enrollment", data_type="string")
class PIIValidator(Validator):
    """
    """
    def __init__(self, on_match: Optional[str] = None, on_fail: Optional[Callable] = None):
        super().__init__(on_match=on_match, on_fail=on_fail)
        
    def validate(self, value: str, metadata: Dict = {}) -> ValidationResult:
        """
        """
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



guardas_eureca = Guard().use(PIIValidator)

try:
    guardas_eureca.parse("A minha matricula é o seguinte: 221199999, busque informaões sobre ela").model_validate
except Exception as e:
    print(e)


@register_validator(name="guardrails/cpf", data_type="string")
class PIIValidatorCPF(Validator):
    def __init__(self, on_match: Optional[str] = None, on_fail: Optional[Callable] = None):
        super().__init__(on_match=on_match, on_fail=on_fail)
        
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


guardas_eureca = Guard().use(PIIValidatorCPF)

try:
    result = guardas_eureca.parse("O meu CPF é o seguinte: 99999999999, busque informaões sobre ele").model_validate
except Exception as e:
    print(e)