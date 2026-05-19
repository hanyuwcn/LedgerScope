from src.config import variable_names
from src.core.base_variable import Variable


class InterestRate(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.FINANCE_INTEREST_RATE


class TaxRate(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.FINANCE_TAX_RATE


class USDToRMB(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.FINANCE_USD_TO_RMB
