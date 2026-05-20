from src.config import variable_names
from src.core.base_model import Model


def calculate_total_expense(**kwargs) -> dict:
    """
    Calculates consolidated operational expenses scaled to a specific monthly horizon.

    Mathematical Formula:
        Expense = (MonthlyRent + MonthlyRenderFee + MonthlyTravelFee) * Months

    Args:
        **kwargs: Arbitrary keyword arguments containing mathematical tracking metrics:

            Optional Keys:
                MONTHS (int/float, optional): The duration factor representing the fiscal timeline
                    horizon being evaluated (e.g., 3 for quarterly, 12 for annual). Defaults to 12.
                EXPENSE_MONTHLY_RENT (float, optional): Monthly real estate lease fees. Defaults to 0.0.
                EXPENSE_RENDER_FEE (float, optional): Monthly infrastructure/rendering overhead. Defaults to 0.0.
                EXPENSE_TRAVEL_FEE (float, optional): Monthly team travel allowances. Defaults to 0.0.

    Returns:
        dict: A dictionary mapping the duration-scaled operating expenses directly to the source-of-truth registry.
            Example: {"Expense": 24000.0}
    """
    # Safely pull operational buckets, dropping back to default metrics if not considered for this analysis
    months = kwargs.get(variable_names.MONTHS, 12)
    monthly_rent = kwargs.get(variable_names.EXPENSE_MONTHLY_RENT, 0.0)
    monthly_render_fee = kwargs.get(variable_names.EXPENSE_RENDER_FEE, 0.0)
    monthly_travel_fee = kwargs.get(variable_names.EXPENSE_TRAVEL_FEE, 0.0)

    # Computes total sum scaled strictly to the requested time horizon
    calculated_expense = (monthly_rent + monthly_render_fee + monthly_travel_fee) * months

    return {variable_names.EXPENSE: calculated_expense}


class ExpenseModel(Model):
    """
    Pipeline calculation block responsible for aggregating individual fixed/variable
    operating expenses and scaling them across flexible calendar durations.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the ExpenseModel with standardized analytical boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking calculation interface logic to output registers
        self._model_function = calculate_total_expense
        self._output_names = [variable_names.EXPENSE]

        # All variables are now optional to support rapid, zero-overhead baseline testing
        self._required_variables = []

        self._optional_variables = [
            variable_names.EXPENSE_MONTHLY_RENT,
            variable_names.EXPENSE_RENDER_FEE,
            variable_names.EXPENSE_TRAVEL_FEE,
            variable_names.MONTHS
        ]
