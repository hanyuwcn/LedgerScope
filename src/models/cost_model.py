from src.config import variable_names
from src.core.base_model import Model


def calculate_total_cost(**kwargs) -> dict:
    """
    Calculates the consolidated total operating cost for the business lifecycle step.

    Mathematical Formula:
        Cost = Cogs + AdvertisingCost + ShippingCost

    Args:
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                COST_COGS (float): Total Cost of Goods Sold evaluated from product supply chains.
                COST_ADVERTISING (float): Total budget allocated toward marketing/customer acquisition channels.

            Optional Keys:
                COST_SHIPPING (float, optional): Operational shipping and fulfillment expenses.
                    Defaults safely to 0.0 under the standard operational assumption that end
                    consumers cover fulfillment fees out-of-pocket.

    Returns:
        dict: A dictionary mapping the consolidated cost calculations directly to the central tracking constant.
            Example: {"Cost": 12500.0}
    """
    cogs = kwargs[variable_names.COST_COGS]
    ads_cost = kwargs[variable_names.COST_ADVERTISING]

    # Safely drops back to 0.0 if the business model defaults shipping coverage to customers
    shipping_cost = kwargs.get(variable_names.COST_SHIPPING, 0.0)

    calculated_cost = cogs + ads_cost + shipping_cost

    return {variable_names.COST: calculated_cost}


class TotalCostModel(Model):
    """
    Pipeline calculation block responsible for aggregating raw product, marketing,
    and logistical fulfillment fees into a centralized total cost metric.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the TotalCostModel with explicit validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional logic and mapping outputs to the central registry
        self._model_function = calculate_total_cost
        self._output_names = [variable_names.COST]

        # Establishing dependencies for the pipeline layer
        self._required_variables = [
            variable_names.COST_COGS,
            variable_names.COST_ADVERTISING
        ]
        self._optional_variables = [
            variable_names.COST_SHIPPING
        ]
