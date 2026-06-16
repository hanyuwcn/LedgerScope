from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_total_expense(variables: dict) -> dict:
    """
    Calculates the aggregated total operating expense for the period.

    Mathematical Formula:
        TotalExpense = ManagementExpense + SellingExpense

    Args:
        variables (dict): Unified context containing all variables,
            resolved by the Model base class (with defaults for optional fields).

    Returns:
        dict: A dictionary mapping the aggregated total expense directly to
            the central pipeline registry.
    """
    total_management_expense = variables[vn.MANAGEMENT_EXPENSE]
    total_selling_expense = variables[vn.SELLING_EXPENSE]

    calculated_total_expense = total_management_expense + total_selling_expense
    return {vn.EXPENSE: calculated_total_expense}


class TotalExpenseModel(Model):
    """
    Pipeline calculation block responsible for aggregating distinct administrative
    and operational cost centers into a single total expense figure.

    Description:
        This model serves as a consolidation anchor, summing management overheads
        and selling expenses. By creating a unified 'EXPENSE' metric, it streamlines
        downstream calculations for net income and profit margin analysis.

    Calculation Equation:
        TotalExpense = ManagementExpense + SellingExpense

        Where:
        - "ManagementExpense" maps to vn.MANAGEMENT_EXPENSE (Optional, default 0.0)
        - "SellingExpense" maps to vn.SELLING_EXPENSE (Optional, default 0.0)
        - "TotalExpense" maps to vn.EXPENSE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the TotalExpenseModel with standard boundary checks.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_total_expense
        self._output_names = [vn.EXPENSE]

        # No specific required inputs; all components are optional with 0.0 defaults
        self._required_variables = []

        self._optional_variables = {
            vn.MANAGEMENT_EXPENSE: 0.0,
            vn.SELLING_EXPENSE: 0.0
        }
