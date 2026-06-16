from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_revenue(variables: dict) -> dict:
    """
    Calculates the gross top-line operational revenue for the specific transactional cycle.

    Mathematical Formula:
        Revenue = UnitFreeOnBoardPrice * UnitsSold * USDToRMB

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated gross top-line revenue to
            its source-of-truth registry key.
            Example: {"Revenue": 48600.0}
    """
    selling_price = variables[vn.UNIT_FOB_PRICE]
    units_sold = variables[vn.UNITS_SOLD]
    usd_to_rmb = variables[vn.USD_TO_RMB]

    calculated_revenue = selling_price * units_sold * usd_to_rmb

    return {vn.REVENUE: calculated_revenue}


class RevenueModel(Model):
    """
    Pipeline calculation block responsible for translating sales volumes and item-level
    pricing structures into a consolidated top-line gross revenue metric.

    Description:
        This model aggregates incoming purchase signals and transactional density profiles
        to compute top-line operating inflows. By factoring in unit volumes and pricing
        denominations, it builds a standardized gross intake baseline used subsequently
        by tax, profitability, and margin expansion evaluation models downstream.

    Calculation Equation:
        Revenue = UnitFreeOnBoardPrice * UnitsSold * USDToRMB

        Where:
        - "UnitFreeOnBoardPrice" maps to vn.UNIT_FOB_PRICE
        - "UnitsSold" maps to vn.UNITS_SOLD
        - "USDToRMB" maps to vn.USD_TO_RMB
        - "Revenue" maps to vn.REVENUE
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
        self._output_names = [vn.REVENUE]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.UNIT_FOB_PRICE,
            vn.UNITS_SOLD,
        ]

        # Migrated from standard list footprint to map defaults transparently
        self._optional_variables = {
            vn.USD_TO_RMB: 1.0
        }
