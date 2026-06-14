from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_cost_of_goods_sold(variables: dict) -> dict:
    """
    Calculates the total Cost of Goods Sold (COGS) based on physical product metrics.

    Mathematical Formula:
        COGS = UnitExWorksPrice * Orders * UnitsPerOrder

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary containing the computed COGS value mapped to
            the source-of-truth key.
            Example: {"COGS": 15000.0}
    """
    purchasing_price = variables[vn.UNIT_EXW]
    orders = variables[vn.ORDERS]
    units_per_order = variables[vn.UNITS_PER_ORDER]

    calculated_cogs = purchasing_price * orders * units_per_order

    return {vn.COGS: calculated_cogs}


class CostOfGoodsSoldModel(Model):
    """
    Pipeline calculation block evaluating supply chain and sales volume to compute raw product cost.

    Description:
        This model evaluates total procurement and supply chain expenditure by processing unit costs
        against baseline transaction volume metrics. It calculates the necessary direct capital
        outlay required to fulfill pipeline orders, allowing margin analysis engines downstream
        to evaluate true gross profit profiles.

    Calculation Equation:
        COGS = Orders * UnitsPerOrder * UnitExWorksPrice

        Where:
        - "Orders" maps to vn.ORDERS
        - "UnitsPerOrder" maps to vn.UNITS_PER_ORDER
        - "UnitExWorksPrice" maps to vn.UNIT_EXW
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
        self._output_names = [vn.COGS]

        # Explicitly enforcing required parameters from your centralized registry
        self._required_variables = [
            vn.UNIT_EXW,
            vn.ORDERS,
            vn.UNITS_PER_ORDER
        ]
