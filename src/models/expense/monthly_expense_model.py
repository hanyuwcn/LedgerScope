from src.config import variable_names
from src.core.base_model import Model


def calculate_monthly_expense(optional_variables: dict, **kwargs) -> dict:
    """
    Aggregates individual fixed and variable operating expenses into a baseline
    monthly run-rate overhead.

    Mathematical Formula:
        MonthlyExpense = RentExpense + RenderExpense + TravelExpense

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing active runtime metrics:

            Optional Keys:
                RentExpense (float): Monthly real estate lease fees.
                RenderExpense (float): Monthly infrastructure/rendering overhead.
                TravelExpense (float): Monthly team travel allowances.

    Returns:
        dict: A dictionary mapping the aggregated monthly running cost to the central tracker.
            Example: {"MonthlyExpense": 2000.0}
    """
    default_rent = optional_variables[variable_names.RENT_EXPENSE]
    default_render = optional_variables[variable_names.RENDER_EXPENSE]
    default_travel = optional_variables[variable_names.TRAVEL_EXPENSE]

    rent = kwargs.get(variable_names.RENT_EXPENSE, default_rent)
    render = kwargs.get(variable_names.RENDER_EXPENSE, default_render)
    travel = kwargs.get(variable_names.TRAVEL_EXPENSE, default_travel)

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
