from src.config import variable_names
from src.core import Variable


class Expense(Variable):
    """
    Represents the general baseline transactional expense variable factor.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.EXPENSE


class MonthlyExpense(Variable):
    """
    Tracks aggregated recurring operational run-rate overhead calculated per period.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.MONTHLY_EXPENSE


class RentExpense(Variable):
    """
    Models fixed space facility lease commitments or regional workspace rental outlays.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.RENT_EXPENSE


class TravelExpense(Variable):
    """
    Captures variable auxiliary travel, logistics, and localized field execution fees.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.TRAVEL_EXPENSE


class RenderExpense(Variable):
    """
    Represents technological or computational asset usage allocation costs.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.RENDER_EXPENSE
