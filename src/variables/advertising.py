from src.config import variable_names as vn
from src.core import Variable


class AdvertisingBudget(Variable):
    """
    Represents the total financial capital allocated for advertisement spend.

    Funnel Role: Top-of-funnel resource input.
    Default Operational Bounds:
        - Minimum: 1500.0
        - Maximum: 3000.0
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.ADVERTISING_COST


class GoogleSearchConversionRate(Variable):
    """
    The efficiency metric tracking traffic-to-lead generation.
    Calculated as the total number of leads divided by total Google Search clicks.

    Funnel Role: Mid-funnel acquisition driver.
    Default Operational Bounds:
        - Minimum: 0.02 (2%)
        - Maximum: 0.06 (6%)
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.CONVERSION_RATE_GOOGLE_SEARCH


class GoogleSearchCostPerClick(Variable):
    """
    The financial cost incurred for each individual click generated
    via Google Search campaigns.

    Funnel Role: Top-of-funnel traffic cost factor.
    Default Operational Bounds:
        - Minimum: 1.80
        - Expected: 2.50
        - Maximum: 3.50
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.CPC_GOOGLE_SEARCH


class GoogleSearchAllocationPercentage(Variable):
    """
    The proportion of the total advertising budget assigned specifically
    to Google Search campaigns.

    Funnel Role: Top-of-funnel capital distribution metric.
    Default Operational Bounds:
        - Minimum: 0.50 (50%)
        - Maximum: 0.70 (70%)
    """

    def __init__(self, min=None, exp=None, max=None):
        super().__init__(min, exp, max)
        self._name = vn.ALLOCATION_GOOGLE_SEARCH
