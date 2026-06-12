from src.config import variable_names
from src.core.base_model import Model


def calculate_total_cost(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the consolidated total operational cost for the business lifecycle step.

    Mathematical Formula:
        TotalCost = COGS + AdvertisingCost + ShippingCost

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                COGS (float): Total Cost of Goods Sold evaluated from product supply chains.

            Optional Keys:
                ADVERTISING_COST (float, optional): Total budget allocated toward marketing channels.
                SHIPPING_COST (float, optional): Operational shipping and fulfillment expenses.

    Returns:
        dict: A dictionary mapping the consolidated cost calculations to the
            central registry key.
            Example: {"TotalCost": 12500.0}
    """
    cogs = kwargs[variable_names.COGS]

    # Dynamically extract values from active runtime args or fallback safely
    ads_cost = kwargs.get(variable_names.ADVERTISING_COST, optional_variables[variable_names.ADVERTISING_COST])
    shipping_cost = kwargs.get(variable_names.SHIPPING_COST, optional_variables[variable_names.SHIPPING_COST])

    calculated_cost = cogs + ads_cost + shipping_cost

    return {variable_names.COST: calculated_cost}


class TotalCostModel(Model):
    """
    Pipeline calculation block responsible for aggregating product, marketing,
    and logistical fulfillment fees into a centralized total operational cost metric.

    Description:
        This model serves as the primary aggregation point for variable operating expenses.
        It unifies baseline product procurement, customer acquisition outlays, and
        logistics into an all-inclusive cost figure, excluding one-time capital
        investments (CAPEX). This metric is critical for down-funnel net margin
        profiling and bottom-line profit modeling.

    Calculation Equation:
        TotalCost = COGS + AdvertisingCost + ShippingCost

        Where:
        - "COGS" maps to variable_names.COGS
        - "AdvertisingCost" maps to variable_names.ADVERTISING_COST
        - "ShippingCost" maps to variable_names.SHIPPING_COST
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the TotalCostModel with explicit validation boundaries.
        """
        super().__init__(input_variables)

        # Hooking functional logic and mapping outputs to the central registry
        self._model_function = calculate_total_cost
        self._output_names = [variable_names.COST]

        # Establishing dependencies for the pipeline layer
        self._required_variables = [
            variable_names.COGS
        ]

        # Map defaults transparently to 0.0 for simulation flexibility
        self._optional_variables = {
            variable_names.ADVERTISING_COST: 0.0,
            variable_names.SHIPPING_COST: 0.0
        }
