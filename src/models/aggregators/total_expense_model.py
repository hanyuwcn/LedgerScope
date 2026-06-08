from src.config import variable_names
from src.core.base_model import Model


def calculate_total_expense_horizon(optional_variables: dict, **kwargs) -> dict:
    """
    Scales the consolidated monthly running overhead across a flexible calendar duration.

    Mathematical Formula:
        Expense = MonthlyExpense * Months

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required calculation drivers:

            Mandatory Keys:
                MonthlyExpense (float): Aggregated running operational cost per period.

            Optional Keys:
                Months (int/float): The time-horizon scale multiplier factor.

    Returns:
        dict: A dictionary mapping the total duration-scaled cost to the source-of-truth registry.
            Example: {"Expense": 24000.0}
    """
    monthly_expense = kwargs[variable_names.MONTHLY_EXPENSE]

    default_months = optional_variables[variable_names.MONTHS]
    months = kwargs.get(variable_names.MONTHS, default_months)

    calculated_total = monthly_expense * months

    return {variable_names.EXPENSE: calculated_total}


class TotalExpenseModel(Model):
    """
    Pipeline calculation block responsible for scaling monthly operational expenditures
    across dynamic calendar macro horizons.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = calculate_total_expense_horizon
        self._output_names = [variable_names.EXPENSE]

        # MonthlyExpense is now strictly required to evaluate the temporal horizon scale
        self._required_variables = [
            variable_names.MONTHLY_EXPENSE
        ]
        self._optional_variables = {
            variable_names.MONTHS: 12
        }
