from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_gross_profit(variables: dict) -> dict:
    """
    Calculates the net operational profit generated within the execution context.

    Mathematical Formula:
        Profit = Revenue - Cogs

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the net profit calculation directly
            to the source-of-truth registry.
            Example: {"GrossProfit": 15000.0}
    """
    revenue = variables[vn.REVENUE]
    cogs = variables[vn.COGS]

    calculated_profit = revenue - cogs

    return {vn.GROSS_PROFIT: calculated_profit}


class GrossProfitModel(Model):
    """
    Pipeline calculation block responsible for subtracting operational costs from gross
    top-line revenue to determine baseline operational profitability.

    Description:
        The Gross Profit Model serves as the foundational financial building block within the
        analytical pipeline, establishing the business engine's fundamental unit economics.
        By executing a direct extraction of Cost of Goods Sold (COGS) from top-line revenue,
        this model isolates raw financial yield before it is influenced by downstream variables
        such as localized corporate tax structures, multi-year fixed asset depreciation schedules,
        or administrative overhead (OpEx).

        Measuring profit at this layer allows analysts to benchmark the direct efficiency of
        sales conversion and product delivery systems across disparate runtime scenarios.

    Calculation Equation:
        Profit = Revenue - Cogs

        Where:
        - "Revenue" maps to vn.REVENUE (Required)
        - "Cogs" maps to vn.COGS (Required)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the GrossProfitModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_gross_profit
        self._output_names = [vn.GROSS_PROFIT]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.REVENUE,
            vn.COGS,
        ]
