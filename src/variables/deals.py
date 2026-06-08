from src.config import variable_names
from src.core import Variable


class Orders(Variable):
    """
    Represents the total volume of successful purchase transactions processed.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.ORDERS


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
        self._name = variable_names.CLOSE_RATE


class UnitExw(Variable):
    """
    Ex Works factory floor base pricing parameter for primary manufacturing tracking.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.UNIT_EXW


class UnitRetail(Variable):
    """
    End-user market retail valuation parameter used for strategic revenue baseline tracking.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.UNIT_RETAIL


class ChannelMarkupRate(Variable):
    """
    Percentage premium captured by distributor networks and ecosystem channel partners.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.CHANNEL_MARKUP_RATE


class ShippingRate(Variable):
    """
    Logistics overhead coefficient mapping the variable cross-border or localized haulage metrics.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.SHIPPING_RATE


class DeductionRate(Variable):
    """
    Combined standard rate modeling statutory deductions, localized levies, or marketplace fees.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.DEDUCTION_RATE


class UnitFob(Variable):
    """
    Free On Board baseline parameter factoring point-of-origin delivery port valuation.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.UNIT_FOB


class UnitsPerOrder(Variable):
    """
    The average quantity of individual products included within a single order transaction.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = variable_names.UNITS_PER_ORDER
