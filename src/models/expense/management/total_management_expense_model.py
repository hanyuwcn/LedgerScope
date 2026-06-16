from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_total_management_expense(variables: dict) -> dict:
    """
    Scales the consolidated monthly running overhead across a flexible calendar duration.

    Mathematical Formula:
        ManagementExpense = MonthlyManagementExpense * Months

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the total duration-scaled cost to the
            source-of-truth registry.
            Example: {"ManagementExpense": 24000.0}
    """
    monthly_management_expense = variables[vn.MONTHLY_MANAGEMENT_EXPENSE]
    months = variables[vn.MONTHS]

    calculated_total_management_expense = monthly_management_expense * months

    return {vn.MANAGEMENT_EXPENSE: calculated_total_management_expense}


class TotalManagementExpenseModel(Model):
    """
    Pipeline calculation block responsible for scaling monthly operational expenditures
    across dynamic calendar macro horizons.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = calculate_total_management_expense
        self._output_names = [vn.MANAGEMENT_EXPENSE]

        self._required_variables = [
            vn.MONTHLY_MANAGEMENT_EXPENSE
        ]
        self._optional_variables = {
            vn.MONTHS: 12
        }
