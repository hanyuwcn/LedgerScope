from src.config import variable_names as vn
from src.core import Variable


class UnitRetailPrice(Variable):
    """
    End-user market retail valuation parameter used for strategic revenue baseline tracking.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_RETAIL_PRICE


class DeductionRate(Variable):
    """
    Combined standard rate modeling statutory deductions, localized levies, or marketplace fees.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.DEDUCTION_RATE


class RetailMarginRate(Variable):
    """
    Percentage premium captured by distributor networks and ecosystem channel partners.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.CHANNEL_MARKUP_RATE


class MerchantFreightRate(Variable):
    """
    Logistics overhead coefficient mapping the variable cross-border or localized haulage metrics by the merchant
    or distributor.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.MERCHANT_FREIGHT_RATE


class UnitMerchantFreightExpense(Variable):
    """
    The calculated monetary cost of logistics per unit, borne by the merchant
    or distributor, often derived from the Unit Retail Price and Freight Rate.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_MERCHANT_FREIGHT_EXPENSE


class UnitTariff(Variable):
    """
    The specific per-unit import duty or tax levied by government authorities,
    impacting the total landed cost of the product.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_TARIFF


class UnitRetailMargin(Variable):
    """
    The absolute monetary profit per unit retained by the merchant after accounting
    for the product cost, freight, and tariff obligations.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_RETAIL_MARGIN
