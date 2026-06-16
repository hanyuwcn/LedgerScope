from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_gross_profit(variables: dict) -> dict:
    """
    Calculates the unit-level gross profit for the Brand.

    Mathematical Formula:
        UnitGrossProfit = GrossProfit / UnitsSold

    Args:
        variables (dict): Unified context containing all mandatory variables,
            resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the computed unit-level
            profitability to the central pipeline registry.
            Example: {"UnitGrossProfit": 15.50}
    """
    profit = variables[vn.GROSS_PROFIT]
    units_sold = variables[vn.UNITS_SOLD]

    # Handle division by zero for scenarios with no sales volume
    if units_sold == 0:
        return {vn.UNIT_GROSS_PROFIT: 0.0}

    calculated_unit_gross_profit = profit / units_sold
    return {vn.UNIT_GROSS_PROFIT: calculated_unit_gross_profit}


class UnitGrossProfitModel(Model):
    """
    Pipeline calculation block responsible for quantifying the unit-level
    gross profit based on aggregate performance.

    Description:
        The Unit Gross Profit represents the normalized profit return for a single
        unit of inventory. By deriving this from total profit and sales volume,
        this model validates the efficiency of the overall price waterfall
        consistency and provides granular visibility into per-unit profitability.

    Calculation Equation:
        UnitGrossProfit = GrossProfit / UnitsSold

        Where:
        - "GrossProfit" maps to vn.GROSS_PROFIT
        - "UnitsSold" maps to vn.UNITS_SOLD
        - "UnitGrossProfit" maps to vn.UNIT_GROSS_PROFIT
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitGrossProfitModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_unit_gross_profit
        self._output_names = [vn.UNIT_GROSS_PROFIT]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.GROSS_PROFIT,
            vn.UNITS_SOLD,
        ]
