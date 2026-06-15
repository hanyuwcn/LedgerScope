from src.config import variable_names as vn
from src.core import Variable


class Months(Variable):
    """
    The number of months to aggregate
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.MONTHS
