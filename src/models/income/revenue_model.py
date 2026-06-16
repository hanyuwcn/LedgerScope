from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_revenue(variables: dict) -> dict:
    """
    Calculates the gross top-line operational revenue in RMB for the
    specific transactional cycle.

    Mathematical Formula:
        Revenue = UnitFobPriceInRMB * UnitsSold

    Args:
        variables (dict): Unified context containing all mandatory
            variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated gross top-line revenue to
            its source-of-truth registry key.
    """
    selling_price = variables[vn.UNIT_FOB_PRICE_IN_RMB]
    units_sold = variables[vn.UNITS_SOLD]

    calculated_revenue = selling_price * units_sold

    return {vn.REVENUE: calculated_revenue}


class RevenueModel(Model):
    """
    Pipeline calculation block responsible for translating sales volumes and
    RMB-denominated pricing structures into a consolidated top-line gross
    revenue metric.

    Description:
        This model aggregates incoming purchase signals and transactional density
        profiles to compute top-line operating inflows. By using pre-converted
        RMB unit prices, it simplifies the calculation baseline for downstream
        profitability and margin analysis.

    Calculation Equation:
        Revenue = UnitFobPriceInRMB * UnitsSold

        Where:
        - "UnitFobPriceInRMB" maps to vn.UNIT_FOB_PRICE_IN_RMB
        - "UnitsSold" maps to vn.UNITS_SOLD
        - "Revenue" maps to vn.REVENUE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the RevenueModel with explicit parameter validation boundaries.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_revenue
        self._output_names = [vn.REVENUE]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.UNIT_FOB_PRICE_IN_RMB,
            vn.UNITS_SOLD,
        ]
