from src.config import variable_names
from src.core import Variable


class Orders(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.DEAL_ORDERS


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


# TODO: change to UnitsPerOrder
class ItemsPerOrder(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.DEAL_ITEMS_PER_ORDER


class SellingPrice(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.DEAL_SELLING_PRICE


class PurchasingPrice(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.DEAL_PURCHASING_PRICE
