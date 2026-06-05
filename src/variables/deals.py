from src.config import variable_names
from src.core import Variable


class Orders(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = variable_names.DEAL_ORDERS


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
