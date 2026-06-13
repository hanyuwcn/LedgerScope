from src.config import variable_names
from src.core.base_model import Model


def calculate_revenue(variables: dict) -> dict:
    """
    Calculates the gross top-line operational revenue for the specific transactional cycle.

    Mathematical Formula:
        Revenue = UnitFob * Orders * UnitsPerOrder * USDToRMB

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated gross top-line revenue to
            its source-of-truth registry key.
            Example: {"REVENUE": 48600.0}
    """
    selling_price = variables[variable_names.UNIT_FOB]
    orders = variables[variable_names.ORDERS]
    items_per_order = variables[variable_names.UNITS_PER_ORDER]
    usd_to_rmb = variables[variable_names.USD_TO_RMB]

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
        Revenue = Orders * UnitsPerOrder * UnitFob * USDToRMB

        Where:
        - "Orders" maps to variable_names.ORDERS
        - "UnitsPerOrder" maps to variable_names.UNITS_PER_ORDER
        - "UnitFob" maps to variable_names.UNIT_FOB
        - "USDToRMB" maps to variable_names.USD_TO_RMB
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
            variable_names.UNIT_FOB,
            variable_names.ORDERS,
            variable_names.UNITS_PER_ORDER
        ]

        # Migrated from standard list footprint to map defaults transparently
        self._optional_variables = {
            variable_names.USD_TO_RMB: 1.0
        }
