from src.config import variable_names
from src.core.base_model import Model


def calculate_profit(**kwargs) -> dict:
    """
    Calculates the net operational profit generated within the execution context.

    Mathematical Formula:
        Profit = Revenue - Cost

    Args:
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                REVENUE (float): Gross top-line operational revenue generated via sales.
                COST (float): Aggregated operating costs, inclusive of product supply chain
                    and marketing acquisition fees.

    Returns:
        dict: A dictionary mapping the net profit calculation directly to the source-of-truth registry.
            Example: {"Profit": 15000.0}
    """
    revenue = kwargs[variable_names.REVENUE]
    cost = kwargs[variable_names.COST]

    calculated_profit = revenue - cost

    # Wrapped securely in a dictionary to satisfy the base model's .update() processor
    return {variable_names.PROFIT: calculated_profit}


class ProfitModel(Model):
    """
    Pipeline calculation block responsible for subtracting operational costs from gross
    top-line revenue to determine net fiscal profitability.
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
        self._output_names = [variable_names.PROFIT]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            variable_names.REVENUE,
            variable_names.COST
        ]
