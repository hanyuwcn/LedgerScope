from src.config import variable_names
from src.core.base_model import Model


def calculate_total_cost(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the consolidated total operating cost for the business lifecycle step,
    incorporating one-time initialization fees alongside active operational variables.

    Mathematical Formula:
        Cost = SetupCost + Cogs + AdvertisingCost + ShippingCost

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                Cogs (float): Total Cost of Goods Sold evaluated from product supply chains.

            Optional Keys:
                SetupCost (float, optional): Initial capital expenditure or infrastructure startup fees.
                AdvertisingCost (float, optional): Total budget allocated toward marketing channels.
                ShippingCost (float, optional): Operational shipping and fulfillment expenses.

    Returns:
        dict: A dictionary mapping the consolidated cost calculations directly to the central tracking constant.
            Example: {"Cost": 12500.0}
    """
    cogs = kwargs[variable_names.COGS]

    # Extract default fallback parameter bounds directly out of the configuration registry map
    default_setup_cost = optional_variables[variable_names.SETUP_COST]
    default_ads_cost = optional_variables[variable_names.ADVERTISING_COST]
    default_shipping_cost = optional_variables[variable_names.SHIPPING_COST]

    # Dynamically extract values from active runtime args or fallback safely
    setup_cost = kwargs.get(variable_names.SETUP_COST, default_setup_cost)
    ads_cost = kwargs.get(variable_names.ADVERTISING_COST, default_ads_cost)
    shipping_cost = kwargs.get(variable_names.SHIPPING_COST, default_shipping_cost)

    calculated_cost = setup_cost + cogs + ads_cost + shipping_cost

    return {variable_names.COST: calculated_cost}


class TotalCostModel(Model):
    """
    Pipeline calculation block responsible for aggregating corporate launch, product,
    marketing, and logistical fulfillment fees into a centralized total cost metric.

    Description:
        This model serves as an aggregation point for both foundational and variable cost
        elements of the operational cycle. It unifies upfront capital or corporate initialization fees,
        baseline product procurement expenses, customer acquisition outlays, and final-mile transport
        logistics into an all-inclusive cost figure. This consolidated output is critically essential
        for down-funnel net margin profiling and bottom-line profit modeling.

    Calculation Equation:
        Cost = SetupCost + Cogs + AdvertisingCost + ShippingCost

        Where:
        - "SetupCost" maps to variable_names.SETUP_COST
        - "Cogs" maps to variable_names.COGS
        - "AdvertisingCost" maps to variable_names.ADVERTISING_COST
        - "ShippingCost" maps to variable_names.SHIPPING_COST
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
            variable_names.COGS
        ]

        # Migrated from standard list footprint to map defaults transparently to 0.0
        self._optional_variables = {
            variable_names.ADVERTISING_COST: 0.0,
            variable_names.SHIPPING_COST: 0.0,
            variable_names.SETUP_COST: 0.0
        }
