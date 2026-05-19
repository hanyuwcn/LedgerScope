from src.config import variable_names
from src.core.base_model import Model


def calculate_project_roi(**kwargs) -> dict:
    """
    Calculates Project Return on Investment (Option A) across all cash outlays.

    Mathematical Formula:
        ROI = NetIncome / (Cost + Expense + CapitalExpenditure)

    Args:
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                NET_INCOME (float): Net operational profit after tax from NetIncomeModel.
                COST (float): Aggregated core operating costs.
                EXPENSE (float): Duration-scaled operational expenses.
                CAPITAL_EXPENDITURE (float): Upfront asset capital investments.

    Returns:
        dict: A dictionary mapping the calculated ROI decimal directly to the registry.
            Example: {"ROI": 0.25} (representing a 25% return)
    """
    net_income = kwargs[variable_names.NET_INCOME]
    cost = kwargs[variable_names.COST]
    expense = kwargs[variable_names.EXPENSE]
    cap_ex = kwargs[variable_names.CAPITAL_EXPENDITURE]

    total_denominational_investment = cost + expense + cap_ex

    # Protect engine against a zero-denominator division crash
    if total_denominational_investment == 0:
        return {variable_names.ROI: 0.0}

    calculated_roi = net_income / total_denominational_investment

    return {variable_names.ROI: calculated_roi}


class RoiModel(Model):
    """
    Pipeline calculation block evaluating overall project efficiency by scaling 
    after-tax net income against cumulative cash outlays.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)

        self._model_function = calculate_project_roi
        self._output_names = [variable_names.ROI]

        self._required_variables = [
            variable_names.NET_INCOME,
            variable_names.COST,
            variable_names.EXPENSE,
            variable_names.CAPITAL_EXPENDITURE
        ]
