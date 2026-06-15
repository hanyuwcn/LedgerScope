from src.config import settings
from src.config import variable_names as vn
from src.core import Variable


class SetupInvestment(Variable):
    """
    Represents the initial capital expenditure required to launch a new company.
    Includes costs such as equipment acquisition, business registration, and
    website infrastructure development.
    """

    def __init__(self, min=10000, exp=20000, max=30000):
        super().__init__(min, exp, max)
        self._name = vn.SETUP_INVESTMENT


class PriceToEarningsRatio(Variable):
    """
    Valuation multiplier capturing market valuation premiums relative to
    earnings metrics. Used to estimate the total company valuation based
    on projected operating income.
    """

    def __init__(self, min=None, exp=settings.DEFAULT_PE_RATIO, max=None):
        super().__init__(min, exp, max)
        self._name = vn.PE_RATIO
