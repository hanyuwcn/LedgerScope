from src.config import EXPENSE, EXPENSE_MONTHLY_RENT, EXPENSE_TRAVEL_FEE, EXPENSE_RENDER_FEE, COST_MANAGEMENT
from src.core import Variable


class Expense(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = EXPENSE

class Rent(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = EXPENSE_MONTHLY_RENT

class TravelFee(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = EXPENSE_TRAVEL_FEE

class RenderFee(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = EXPENSE_RENDER_FEE