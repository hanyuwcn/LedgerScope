from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_total_cost(variables: dict) -> dict:
    """
    Calculates the consolidated total operational cost for the business lifecycle step.

    Mathematical Formula:
        TotalCost = COGS + AdvertisingCost + ShippingCost

    Args:
        variables (dict): Unified execution context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the consolidated cost to the central tracking constant.
            Example: {"TotalCost": 12500.0}
    """
    cogs = variables[vn.COGS]
    ads_cost = variables[vn.ADVERTISING_COST]
    shipping_cost = variables[vn.SHIPPING_COST]

    calculated_cost = cogs + ads_cost + shipping_cost

    return {vn.COST: calculated_cost}


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
        - "COGS" maps to vn.COGS
        - "AdvertisingCost" maps to vn.ADVERTISING_COST
        - "ShippingCost" maps to vn.SHIPPING_COST
    """

    def __init__(self, input_variables: dict = None):
        """Initializes the TotalCostModel with explicit validation boundaries."""
        super().__init__(input_variables)

        self._model_function = calculate_total_cost
        self._output_names = [vn.COST]

        self._required_variables = [
            vn.COGS
        ]

        self._optional_variables = {
            vn.ADVERTISING_COST: 0.0,
            vn.SHIPPING_COST: 0.0
        }
