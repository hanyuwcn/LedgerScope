from src.config import variable_names
from src.core.base_model import Model


def calculate_cost_of_goods_sold(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the total Cost of Goods Sold (COGS) based on physical product metrics.

    Mathematical Formula:
        COGS = PurchasingPrice * Orders * ItemsPerOrder

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
            Note: This specific model implementation does not require optional parameters,
            but accepts the argument to maintain base interface signature compliance.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                DEAL_PURCHASING_PRICE (float): The unit cost to acquire a single product item.
                DEAL_ORDERS (int/float): Total transaction orders generated.
                DEAL_ITEMS_PER_ORDER (int/float): The average volume of items per transaction order.

    Returns:
        dict: A dictionary containing the computed COGS value mapped to the source-of-truth key.
            Example: {"Cogs": 15000.0}
    """
    purchasing_price = kwargs[variable_names.DEAL_PURCHASING_PRICE]
    orders = kwargs[variable_names.DEAL_ORDERS]
    items_per_order = kwargs[variable_names.DEAL_ITEMS_PER_ORDER]

    calculated_cogs = purchasing_price * orders * items_per_order

    # Wrapped securely in a dictionary to satisfy the base model's .update() processor
    return {variable_names.COST_COGS: calculated_cogs}


class CostOfGoodsSoldModel(Model):
    """
    Pipeline calculation block evaluating supply chain and sales volume to compute raw product cost.

    Description:
        This model evaluates total procurement and supply chain expenditure by processing unit costs
        against baseline transaction volume metrics. It calculates the necessary direct capital
        outlay required to fulfill pipeline orders, allowing margin analysis engines downstream
        to evaluate true gross profit profiles.

    Calculation Equation:
        COGS = Number of Orders * Average number of items per order * average price of item(a.k.a PurchasingPrice)

        Where:
        - "Number of Orders" maps to DEAL_ORDERS
        - "Average number of items per order" maps to DEAL_ITEMS_PER_ORDER
        - "average price of item(a.k.a PurchasingPrice)" maps to DEAL_PURCHASING_PRICE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the CostOfGoodsSoldModel with explicit tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking calculation logic and specifying the correct output variable
        self._model_function = calculate_cost_of_goods_sold
        self._output_names = [variable_names.COST_COGS]

        # Explicitly enforcing required parameters from your centralized registry
        self._required_variables = [
            variable_names.DEAL_PURCHASING_PRICE,
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_ITEMS_PER_ORDER
        ]
