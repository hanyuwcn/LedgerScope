from src.config import variable_names
from src.core import Variable


class Cost(Variable):
    """
    Represents the baseline operational or variable cost structure.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.COST


class AdvertisingCost(Variable):
    """
    Tracks auxiliary platform-specific or legacy performance advertisement costs.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.ADVERTISING_COST


class SetupCost(Variable):
    """
    Models one-time fixed initialization or infrastructure setup capital overhead.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.SETUP_COST
