import datetime as dt

from guardrails.validators import (register_validator, Validator, FailResult, ValidationResult, PassResult)
from typing import Dict, Optional, Callable
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern

@register_validator(name="guardrails/enrollment", data_type="string")
class MatriculaValidator(Validator):
    """
        Validador customizado que valida a presença de uma matrícula no texto
    """
    def __init__(self, on_match: Optional[str] = None, on_fail: Optional[Callable] = None):
        super().__init__(on_match=on_match, on_fail=on_fail)
        
    def validate(self, value: str, metadata: Dict = {}) -> ValidationResult:
        """
            Verifica se há alguma matrícula no texto fornecido.

            Args:
                value: string
                metadata: dicionário de metadados
            
            Returns:
               PassResult: passou na validação
               FailResult: não passou na validação
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