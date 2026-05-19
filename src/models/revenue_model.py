from src.config import variable_names
from src.core.base_model import Model


def calculate_revenue(**kwargs) -> dict:
    """
    Calculates the gross top-line operational revenue for the specific transactional cycle.

    Mathematical Formula:
        Revenue = SellingPrice * Orders * ItemsPerOrder * USDToRMB

    Args:
        **kwargs: Arbitrary keyword arguments containing required mathematical inputs:

            Mandatory Keys:
                DEAL_SELLING_PRICE (float): The retail selling price per individual product unit.
                DEAL_ORDERS (int/float): The total transaction orders generated via acquisition channels.
                DEAL_ITEMS_PER_ORDER (int/float): The average volume of items purchased per distinct order.

            Optional Keys:
                FINANCE_USD_TO_RMB (float, optional): Cross-border currency conversion rate.
                    Utilized to scale top-line metrics if pricing values are tracked in USD but
                    the ledger currency is localized to RMB. Defaults safely to 1.0 if omitted.

    Returns:
        dict: A dictionary mapping the calculated gross top-line revenue to its source-of-truth registry key.
            Example: {"Revenue": 48600.0}
    """
    selling_price = kwargs[variable_names.DEAL_SELLING_PRICE]
    orders = kwargs[variable_names.DEAL_ORDERS]
    items_per_order = kwargs[variable_names.DEAL_ITEMS_PER_ORDER]

    # Defaults to 1.0 if the calculations remain purely within a single domestic currency field
    usd_to_rmb = kwargs.get(variable_names.FINANCE_USD_TO_RMB, 1.0)

    calculated_revenue = selling_price * orders * items_per_order * usd_to_rmb

    return {variable_names.REVENUE: calculated_revenue}


class RevenueModel(Model):
    """
    Pipeline calculation block responsible for translating sales volumes and item-level pricing
    structures into a consolidated top-line gross revenue metric.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the RevenueModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_revenue
        self._output_names = [variable_names.REVENUE]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            variable_names.DEAL_SELLING_PRICE,
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_ITEMS_PER_ORDER
        ]
        self._optional_variables = [
            variable_names.FINANCE_USD_TO_RMB
        ]
