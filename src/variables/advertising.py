from src.config import variable_names
from src.core import Variable


class AdvertisingBudget(Variable):
    """
    Represents the total financial capital allocated for advertisement spend.

    Funnel Role: Top-of-funnel resource input.
    Default Operational Bounds:
        - Minimum: 1500.0
        - Maximum: 3000.0
    """

    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.COST_ADVERTISING


class GoogleSearchConversionRate(Variable):
    """
    The efficiency metric tracking traffic-to-lead generation.
    Calculated as the total number of leads divided by total Google Search clicks.

    Funnel Role: Mid-funnel acquisition driver.
    Default Operational Bounds:
        - Minimum: 0.02 (2%)
        - Maximum: 0.06 (6%)
    """

    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.CONVERSION_RATE_GOOGLE_SEARCH


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

    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.CPC_GOOGLE_SEARCH


class GoogleSearchAllocationPercentage(Variable):
    """
    The proportion of the total advertising budget assigned specifically
    to Google Search campaigns.

    Funnel Role: Top-of-funnel capital distribution metric.
    Default Operational Bounds:
        - Minimum: 0.50 (50%)
        - Maximum: 0.70 (70%)
    """

    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.ALLOCATION_GOOGLE_SEARCH


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

    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.CLOSE_RATE
