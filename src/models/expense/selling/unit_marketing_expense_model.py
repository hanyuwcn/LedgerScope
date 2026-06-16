from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_marketing_expense(variables: dict) -> dict:
    """
    Calculates the unit-level marketing expense per unit sold.

    Mathematical Formula:
        UnitMarketingExpense = TotalMarketingExpense / UnitsSold

    Args:
        variables (dict): Unified context containing all mandatory variables,
            resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated unit marketing expense
            directly to its source-of-truth registry key.
    """
    total_marketing_expense = variables[vn.MARKETING_EXPENSE]
    units_sold = variables[vn.UNITS_SOLD]

    # Protect engine against a zero-denominator division crash
    if units_sold == 0:
        return {vn.UNIT_MARKETING_EXPENSE: 0.0}

    calculated_unit_marketing_expense = total_marketing_expense / units_sold
    return {vn.UNIT_MARKETING_EXPENSE: calculated_unit_marketing_expense}


class UnitMarketingExpenseModel(Model):
    """
    Pipeline calculation block responsible for normalizing total marketing
    outlays across individual units sold.

    Description:
        This model quantifies the marketing cost burden per unit. By allocating
        aggregate marketing expenditures against sales volume, it provides
        visibility into the efficiency of top-of-funnel spend relative to
        individual item performance.

    Calculation Equation:
        UnitMarketingExpense = TotalMarketingExpense / UnitsSold

        Where:
        - "TotalMarketingExpense" maps to vn.MARKETING_EXPENSE
        - "UnitsSold" maps to vn.UNITS_SOLD
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitMarketingExpenseModel with standard boundary checks.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_unit_marketing_expense
        self._output_names = [vn.UNIT_MARKETING_EXPENSE]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.MARKETING_EXPENSE,
            vn.UNITS_SOLD,
        ]
