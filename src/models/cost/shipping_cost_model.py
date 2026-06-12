from src.config import variable_names
from src.core.base_model import Model


def calculate_shipping_cost(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the consolidated shipping (freight) cost for unit-level logistics.

    This function derives the total logistics overhead by applying a variable
    shipping rate against the product's retail footprint, adjusted for volume
    multipliers and currency conversion factors (USD to RMB) for localized
    cost reporting.

    Mathematical Formula:
        ShippingCost = RetailPrice * USDtoRMB * ShippingRate * Orders * UnitsPerOrder

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required mathematical inputs:

            Mandatory Keys:
                UNIT_RETAIL (float): The market retail price used as the base for rate calculations.
                ORDERS (float): Total number of transaction orders processed.
                UNITS_PER_ORDER (float): Average quantity of units contained per order.

            Optional Keys:
                SHIPPING_RATE (float, optional): The freight cost percentage applied
                    to the unit price. Defaults to 0.0.
                USD_TO_RMB (float, optional): The currency conversion multiplier to
                    translate costs from USD to RMB. Defaults to 1.0.

    Returns:
        dict: A single-element dictionary mapping the computed aggregate shipping
            cost to the central pipeline registry.
            Example: {"SHIPPING_COST": 1025.50}
    """
    unit_retail_price = kwargs[variable_names.UNIT_RETAIL]
    orders = kwargs[variable_names.ORDERS]
    units_per_order = kwargs[variable_names.UNITS_PER_ORDER]

    # Dynamically extract values from active runtime args or fallback safely
    shipping_rate = kwargs.get(variable_names.SHIPPING_RATE, optional_variables[variable_names.SHIPPING_RATE])
    usd_to_rmb = kwargs.get(variable_names.USD_TO_RMB, optional_variables[variable_names.USD_TO_RMB])

    total_shipping_cost = unit_retail_price * usd_to_rmb * shipping_rate * orders * units_per_order

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