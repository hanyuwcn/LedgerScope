from src.config import variable_names
from src.core.base_model import Model


def calculate_revenue(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the gross top-line operational revenue for the specific transactional cycle.

    Mathematical Formula:
        Revenue = SellingPrice * Orders * ItemsPerOrder * USDToRMB

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required mathematical inputs:

            Mandatory Keys:
                DEAL_SELLING_PRICE (float): The retail selling price per individual product unit.
                DEAL_ORDERS (int/float): The total transaction orders generated via acquisition channels.
                DEAL_ITEMS_PER_ORDER (int/float): The average volume of items purchased per distinct order.

            Optional Keys:
                FINANCE_USD_TO_RMB (float, optional): Cross-border currency conversion rate.
                    Utilized to scale top-line metrics if pricing values are tracked in USD but
                    the ledger currency is localized to RMB.

    Returns:
        dict: A dictionary mapping the calculated gross top-line revenue to its source-of-truth registry key.
            Example: {"Revenue": 48600.0}
    """
    selling_price = kwargs[variable_names.DEAL_SELLING_PRICE]
    orders = kwargs[variable_names.DEAL_ORDERS]
    items_per_order = kwargs[variable_names.DEAL_ITEMS_PER_ORDER]

    # Pull the default fallback exchange rate from the base configuration parameter registry
    default_usd_to_rmb = optional_variables[variable_names.FINANCE_USD_TO_RMB]
    usd_to_rmb = kwargs.get(variable_names.FINANCE_USD_TO_RMB, default_usd_to_rmb)

    calculated_revenue = selling_price * orders * items_per_order * usd_to_rmb

    return {variable_names.REVENUE: calculated_revenue}


class RevenueModel(Model):
    """
    Pipeline calculation block responsible for translating sales volumes and item-level pricing
    structures into a consolidated top-line gross revenue metric.

    Description:
        This model aggregates incoming purchase signals and transactional density profiles to
        compute top-line operating inflows. By factoring in unit volume volumes and pricing
        denominations, it builds a standardized gross intake baseline used subsequently by tax,
        profitability, and margin expansion evaluation models downstream.

    Calculation Equation:
        Revenue = numbers of orders * number of items per order * average sellingPrice

        Where:
        - "numbers of orders" maps to DEAL_ORDERS
        - "number of items per order" maps to DEAL_ITEMS_PER_ORDER
        - "average sellingPrice" maps to DEAL_SELLING_PRICE
        - Note: The formula also integrates FINANCE_USD_TO_RMB to handle cross-border localization.
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

        # Migrated from standard list footprint to map defaults transparently
        self._optional_variables = {
            variable_names.FINANCE_USD_TO_RMB: 1.0
        }
