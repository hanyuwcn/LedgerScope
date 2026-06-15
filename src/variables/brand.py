from src.config import variable_names as vn
from src.core import Variable


class Orders(Variable):
    """
    Represents the total volume of successful purchase transactions processed.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.ORDERS


class CloseRate(Variable):
    """
    The downstream conversion efficiency tracking lead-to-sale generation.
    Calculated as the total number of processed orders divided by total leads.

    Funnel Role: Bottom-of-funnel sales conversion driver.
    Default Operational Bounds:
        - Minimum: 0.08 (8%)
        - Expected: 0.12 (12%)
        - Maximum: 0.18 (18%)
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.CLOSE_RATE


class UnitsPerOrder(Variable):
    """
    The average quantity of individual products included within a single order transaction.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNITS_PER_ORDER


class UnitsSold(Variable):
    """
    The total aggregate quantity of units distributed to customers across all
    channels during the reporting period. Used as the primary basis for
    calculating unit-level expense allocations.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNITS_SOLD


class UnitExwPrice(Variable):
    """
    Ex Works factory floor base pricing parameter. Represents the direct unit cost
    of manufacturing or procurement, excluding shipping, tariffs, and marketing.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_EXW_PRICE


class UnitFobPrice(Variable):
    """
    Free On Board baseline parameter. Represents the Brand's net unit revenue
    received after channel deductions (excluding freight, tariffs, and markup).
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_FOB_PRICE
