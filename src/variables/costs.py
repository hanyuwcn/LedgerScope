from src.config import variable_names as vn
from src.core import Variable


class Cost(Variable):
    """
    Represents the baseline operational or variable cost structure.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.COST


class AdvertisingCost(Variable):
    """
    Tracks auxiliary platform-specific or legacy performance advertisement costs.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.ADVERTISING_COST


class SetupCost(Variable):
    """
    Models one-time fixed initialization or infrastructure setup capital overhead.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.SETUP_COST
