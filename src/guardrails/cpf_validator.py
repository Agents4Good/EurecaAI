import re

from guardrails.validators import (register_validator, Validator, FailResult, ValidationResult, PassResult)
from typing import Dict, Optional, Callable

@register_validator(name="guardrails/cpf", data_type="string")
class CPFValidator(Validator):
    def __init__(self, on_match: Optional[str] = None, on_fail: Optional[Callable] = None):
        super().__init__(on_match=on_match, on_fail=on_fail)
        
    def validate(self, value: str, metadata: Dict = {}) -> ValidationResult:
        results = self.replace_valid_cpfs(value)

        if "<CPF>" in results:
            return FailResult(error_message=results)
        return PassResult()
    
    def validate_digit_verificator(self, cpf_user):
        if len(set(cpf_user)) == 1: return False
        
        cpf = cpf_user[:9]
        sum = 0
        for i in range(1, len(cpf) + 1):
            sum += i * int(cpf[i - 1])
        first_digit_verificator = sum % 11

        if first_digit_verificator == 10:
            first_digit_verificator = 0


        sum = 0
        cpf = cpf + str(first_digit_verificator)
        for i in range(len(cpf)):
            sum += i * int(cpf[i])
        second_digit_verificator = sum % 11

        if second_digit_verificator == 10:
            second_digit_verificator = 0

        cpf = cpf[:9] + str(first_digit_verificator) + str(second_digit_verificator)
        return cpf == cpf_user


    def replace_valid_cpfs(self, text):
        cpf_pattern =r"\b\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{3}[^a-zA-Z]*\d{2}\b"

        def validate_and_replace(match):
            cpf = match.group(0)
            cpf_numbers = re.sub(r"[^\d]", "", cpf)

            if self.validate_digit_verificator(cpf_numbers):
                return "<CPF>"
            return cpf

        return re.sub(cpf_pattern, validate_and_replace, text)