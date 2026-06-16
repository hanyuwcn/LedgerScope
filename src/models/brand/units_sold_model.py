from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_units_sold(variables: dict) -> dict:
    """
    Calculates total aggregate volume of units sold across all transactions.

    Mathematical Formula:
        UnitsSold = Orders * UnitsPerOrder

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the computed total unit volume
            to the master registry key signature.
    """
    orders = variables[vn.ORDERS]
    units_per_order = variables[vn.UNITS_PER_ORDER]

    # Corrected the calculation logic: Orders * UnitsPerOrder
    calculated_units_sold = orders * units_per_order

    return {vn.UNITS_SOLD: calculated_units_sold}


class UnitsSoldModel(Model):
    """
    Pipeline calculation block responsible for converting transaction volume
    into aggregate unit output.

    Description:
        This model serves as the bridge between order-level transaction metrics
        and supply chain requirement planning. It aggregates disparate order
        signals into a single cumulative unit demand figure.

    Calculation Equation:
        UnitsSold = Orders * UnitsPerOrder

        Where:
        - "Orders" maps to vn.ORDERS
        - "UnitsPerOrder" maps to vn.UNITS_PER_ORDER
        - "UnitsSold" maps to vn.UNITS_SOLD
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitsSoldModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_units_sold
        self._output_names = [vn.UNITS_SOLD]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.ORDERS,
            vn.UNITS_PER_ORDER,
        ]
