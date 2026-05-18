from src.core.base_variable import Variable
from src.config.variable_names import FINANCE_INTEREST_RATE, FINANCE_TAX_RATE, FINANCE_USD_TO_RMB

class InterestRate(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = FINANCE_INTEREST_RATE

class TaxRate(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = FINANCE_TAX_RATE

class USDToRMB(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = FINANCE_USD_TO_RMB