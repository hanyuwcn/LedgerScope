from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_profit(variables: dict) -> dict:
    """
    Calculates the net operational profit generated within the execution context.

    Mathematical Formula:
        Profit = Revenue - Cost

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the net profit calculation directly
            to the source-of-truth registry.
            Example: {"PROFIT": 15000.0}
    """
    revenue = variables[vn.REVENUE]
    cost = variables[vn.COST]

    calculated_profit = revenue - cost

    return {vn.PROFIT: calculated_profit}


class ProfitModel(Model):
    """
    Pipeline calculation block responsible for subtracting operational costs from gross
    top-line revenue to determine baseline operational profitability.

    Description:
        The Profit Model serves as the foundational financial building block within the
        analytical pipeline, establishing the business engine's fundamental unit economics.
        By executing a direct extraction of aggregated operating costs from top-line revenue,
        this model isolates raw financial yield before it is influenced by downstream variables
        such as localized corporate tax structures, multi-year fixed asset depreciation schedules,
        or administrative overhead (OpEx).

        Measuring profit at this layer allows analysts to benchmark the direct efficiency of
        sales conversion and product delivery systems across disparate runtime scenarios. If
        this layer produces a negative value (net loss), it signals a core structural deficit
        in pricing strategy, production scaling, or direct customer acquisition efficiency.

    Calculation Equation:
        profit = revenue - cost

        Where:
        - "revenue" maps to REVENUE (Required)
        - "cost" maps to COST (Required)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the ProfitModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_profit
        self._output_names = [vn.PROFIT]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.REVENUE,
            vn.COST
        ]
