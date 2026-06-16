from src.config import variable_names as vn
from src.core import Variable


class Expense(Variable):
    """
    Represents the general baseline transactional expense variable factor.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.EXPENSE


#### Management Expense


class RentExpense(Variable):
    """
    Models fixed space facility lease commitments or regional workspace rental outlays.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.RENT_EXPENSE


class RenderExpense(Variable):
    """
    Represents technological or computational asset usage allocation costs.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.RENDER_EXPENSE


class TravelExpense(Variable):
    """
    Captures variable auxiliary travel, logistics, and localized field execution fees.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.TRAVEL_EXPENSE


class MonthlyManagementExpense(Variable):
    """
    Tracks aggregated recurring operational run-rate overhead calculated per period.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.MONTHLY_MANAGEMENT_EXPENSE


#### Selling Expense
class MarketingExpense(Variable):
    """
    Represents the total aggregate budget allocated to promotional and brand awareness
    activities for the period.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.MARKETING_EXPENSE


class UnitMarketingExpense(Variable):
    """
    Models the portion of marketing expenditure attributed to a single unit, calculated
    by dividing total marketing spend by units sold.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.UNIT_MARKETING_EXPENSE


class AdvertisingExpense(Variable):
    """
    Tracks direct expenditures specifically related to paid acquisition channels
    (e.g., search, social media, display ads).
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.ADVERTISING_EXPENSE


class BrandFreightExpense(Variable):
    """
    Captures the total aggregate logistics and shipping costs incurred by the Brand
    for the fulfillment of orders during the period.
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.BRAND_FREIGHT_EXPENSE
