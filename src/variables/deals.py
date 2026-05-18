from src.config.variable_names import DEAL_ORDERS, DEAL_ITEMS_PER_ORDER, DEAL_SELLING_PRICE, DEAL_PURCHASING_PRICE
from src.core import Variable


class Orders(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = DEAL_ORDERS


class ItemsPerOrder(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = DEAL_ITEMS_PER_ORDER


class SellingPrice(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = DEAL_SELLING_PRICE


class PurchasingPrice(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = DEAL_PURCHASING_PRICE
