from src.config import variable_names
from src.core.base_model import Model


def calculate_net_income(**kwargs) -> dict:
    """
    Calculates the Net Income After Tax (NOPAT) for the execution context.

    Mathematical Formula:
        NetIncome = (Revenue - Cost - Expense - Depreciation) * (1 - TaxRate)

    Args:
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                REVENUE (float): Gross top-line operational revenue.
                COST (float): Aggregated core operating costs (COGS + Marketing).
                EXPENSE (float): Duration-scaled operational expenses (OPEX).
                DEPRECIATION (float): Non-cash asset depreciation charges.

            Optional Keys:
                FINANCE_TAX_RATE (float, optional): Corporate tax rate multiplier.
                    Defaults safely to 0.0 if evaluating pre-tax scenarios.

    Returns:
        dict: A dictionary mapping the net income directly to its registry key.
            Example: {"NetIncome": 7600.0}
    """
    revenue = kwargs[variable_names.REVENUE]
    cost = kwargs[variable_names.COST]
    expense = kwargs[variable_names.EXPENSE]
    depreciation = kwargs[variable_names.DEPRECIATION]

    tax_rate = kwargs.get(variable_names.FINANCE_TAX_RATE, 0.0)

    # Core corporate accounting math
    pre_tax_income = revenue - cost - expense - depreciation
    calculated_net_income = pre_tax_income * (1.0 - tax_rate)

    return {variable_names.NET_INCOME: calculated_net_income}


class NetIncomeModel(Model):
    """
    Pipeline calculation block responsible for evaluating net profitability
    by deducting operating costs, overhead, and taxes from gross revenue.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)

        self._model_function = calculate_net_income
        self._output_names = [variable_names.NET_INCOME]

        self._required_variables = [
            variable_names.REVENUE,
            variable_names.COST,
            variable_names.EXPENSE,
            variable_names.DEPRECIATION
        ]
        self._optional_variables = [
            variable_names.FINANCE_TAX_RATE
        ]
