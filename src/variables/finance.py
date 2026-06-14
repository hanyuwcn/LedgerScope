from src.config import variable_names as vn, settings
from src.core.base_variable import Variable


class InterestRate(Variable):
    """
    Represents the cost of capital or financing interest penalty adjustments.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.INTEREST_RATE


class TaxRate(Variable):
    """
    Models corporate statutory tax rates applied against taxable net operational margin income.
    """

    def __init__(self, min=None, exp=settings.DEFAULT_TAX_RATE, max=None):
        super().__init__(min, exp, max)
        self._name = vn.TAX_RATE


class USDToRMB(Variable):
    """
    Currency conversion coefficient mapping cross-border financial translation states.
    """

    def __init__(self, min=None, exp=settings.DEFAULT_CURRENCY_RATE, max=None):
        super().__init__(min, exp, max)
        self._name = vn.USD_TO_RMB


class TariffRate(Variable):
    """
    Represents the macro-economic import customs duty rate applied to incoming product shipments.
    """

    def __init__(self, min=None, exp=settings.DEFAULT_TARIFF_RATE, max=None):
        super().__init__(min, exp, max)
        self._name = vn.TARIFF_RATE


class PriceToEarningsRatio(Variable):
    """
    Valuation multiplier capturing market valuation premiums relative to earnings metrics.
    """

    def __init__(self, min=None, exp=settings.DEFAULT_PE_RATIO, max=None):
        super().__init__(min, exp, max)
        self._name = vn.PE_RATIO
