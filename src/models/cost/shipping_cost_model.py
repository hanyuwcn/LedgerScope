from src.config import variable_names
from src.core.base_model import Model


def calculate_shipping_cost(variables: dict) -> dict:
    """
    Calculates the consolidated shipping (freight) cost for unit-level logistics.

    Mathematical Formula:
        ShippingCost = RetailPrice * USDtoRMB * ShippingRate * Orders * UnitsPerOrder

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the computed aggregate shipping
            cost to the central pipeline registry.
            Example: {"SHIPPING_COST": 1025.50}
    """
    unit_retail_price = variables[variable_names.UNIT_RETAIL]
    orders = variables[variable_names.ORDERS]
    units_per_order = variables[variable_names.UNITS_PER_ORDER]
    shipping_rate = variables[variable_names.SHIPPING_RATE]
    usd_to_rmb = variables[variable_names.USD_TO_RMB]

    total_shipping_cost = (
            unit_retail_price * usd_to_rmb * shipping_rate * orders * units_per_order
    )

    return {variable_names.SHIPPING_COST: total_shipping_cost}


class ShippingCostModel(Model):
    """
    Pipeline calculation block responsible for assessing unit-level freight logistics.

    Description:
        This model acts as an essential expense-side node within the pipeline. It
        calculates total shipping burden, enabling accurate assessment of gross
        margins by accounting for the variable costs of moving inventory through
        the fulfillment ecosystem, including currency-adjusted freight overhead.

    Calculation Equation:
        ShippingCost = RetailPrice * USDtoRMB * ShippingRate * Orders * UnitsPerOrder

        Where:
        - "RetailPrice" maps to variable_names.UNIT_RETAIL
        - "USDtoRMB" maps to variable_names.USD_TO_RMB
        - "ShippingRate" maps to variable_names.SHIPPING_RATE
        - "Orders" maps to variable_names.ORDERS
        - "UnitsPerOrder" maps to variable_names.UNITS_PER_ORDER
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the ShippingCostModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional logic and mapping outputs to the central registry
        self._model_function = calculate_shipping_cost
        self._output_names = [variable_names.SHIPPING_COST]

        # Establishing dependencies for the pipeline layer
        self._required_variables = [
            variable_names.UNIT_RETAIL,
            variable_names.ORDERS,
            variable_names.UNITS_PER_ORDER
        ]

        # Mapping defaults transparently to facilitate baseline logistics simulations
        self._optional_variables = {
            variable_names.SHIPPING_RATE: 0.0,
            variable_names.USD_TO_RMB: 1.0
        }
