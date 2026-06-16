from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_fixed_overhead_expense(variables: dict) -> dict:
    """
    Calculates the unit-level fixed overhead (management fee) per unit sold.

    Mathematical Formula:
        UnitFixedOverheadExpense = ManagementExpense / UnitsSold

    Args:
        variables (dict): Unified context containing all mandatory variables,
            resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated unit fixed overhead expense
            directly to its source-of-truth registry key.
            Example: {"UNIT_FIXED_OVERHEAD_EXPENSE": 2.50}
    """
    total_management_expense = variables[vn.MANAGEMENT_EXPENSE]
    units_sold = variables[vn.UNITS_SOLD]

    # Protect engine against a zero-denominator division crash
    if units_sold == 0:
        return {vn.UNIT_FIXED_OVERHEAD_EXPENSE: 0.0}

    calculated_unit_fixed_overhead_expense = total_management_expense / units_sold
    return {vn.UNIT_FIXED_OVERHEAD_EXPENSE: calculated_unit_fixed_overhead_expense}


class UnitFixedOverheadExpenseModel(Model):
    """
    Pipeline calculation block responsible for distributing total management
    overheads across individual units sold.

    Description:
        This model quantifies the fixed overhead burden per unit. By allocating
        aggregate management expenses based on sales volume, it allows the brand
        to visualize the dilution of fixed administrative costs as operations scale.

    Calculation Equation:
        UnitFixedOverheadExpense = ManagementExpense / UnitsSold

        Where:
        - "ManagementExpense" maps to vn.MANAGEMENT_EXPENSE (Required)
        - "UnitsSold" maps to vn.UNITS_SOLD (Required)
        - "UnitFixedOverheadExpense" maps to vn.UNIT_FIXED_OVERHEAD_EXPENSE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitFixedOverheadExpenseModel with standardized accounting boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_unit_fixed_overhead_expense
        self._output_names = [vn.UNIT_FIXED_OVERHEAD_EXPENSE]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.MANAGEMENT_EXPENSE,
            vn.UNITS_SOLD,
        ]

        self._optional_variables = {}
