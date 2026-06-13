from src.config import variable_names
from src.core.base_model import Model


def calculate_monthly_expense(variables: dict) -> dict:
    """
    Aggregates individual fixed and variable operating expenses into a baseline
    monthly run-rate overhead.

    Mathematical Formula:
        MonthlyExpense = RentExpense + RenderExpense + TravelExpense

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the aggregated monthly running cost to the
            central tracker.
            Example: {"MONTHLY_EXPENSE": 2000.0}
    """
    rent = variables[variable_names.RENT_EXPENSE]
    render = variables[variable_names.RENDER_EXPENSE]
    travel = variables[variable_names.TRAVEL_EXPENSE]

    calculated_monthly = rent + render + travel

    return {variable_names.MONTHLY_EXPENSE: calculated_monthly}


class MonthlyExpenseModel(Model):
    """
    Pipeline calculation block responsible for combining localized operational overheads
    into a unified monthly run-rate figure.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = calculate_monthly_expense
        self._output_names = [variable_names.MONTHLY_EXPENSE]
        self._required_variables = []
        self._optional_variables = {
            variable_names.RENT_EXPENSE: 0.0,
            variable_names.RENDER_EXPENSE: 0.0,
            variable_names.TRAVEL_EXPENSE: 0.0,
        }
