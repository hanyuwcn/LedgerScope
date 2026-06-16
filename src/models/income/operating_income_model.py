from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_operating_income(variables: dict) -> dict:
    """
    Calculates the Operating Income for the execution context.

    Mathematical Formula:
        OperatingIncome = Revenue - COGS - Expense - Depreciation

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the operating income metric directly to
            its source-of-truth registry key.
            Example: {"OPERATING_INCOME": 7600.0}
    """
    revenue = variables[vn.REVENUE]
    cogs = variables[vn.COGS]
    expense = variables[vn.EXPENSE]
    depreciation = variables[vn.DEPRECIATION]

    # Calculate operating income by deducting costs and depreciation from revenue
    calculated_operating_income = revenue - cogs - expense - depreciation

    return {vn.OPERATING_INCOME: calculated_operating_income}


class OperatingIncomeModel(Model):
    """
    Pipeline calculation block responsible for evaluating operating profitability.

    Description:
        Operating Income represents the measure of a business unit's profitability
        from its core business operations. This model deducts primary cost of goods
        sold (COGS), operating expenses (OpEx), and non-cash asset depreciation
        adjustments from gross top-line revenue.

    Calculation Equation:
        OperatingIncome = Revenue - COGS - Expense - Depreciation

        Where:
        - "Revenue" maps to vn.REVENUE
        - "COGS" maps to vn.COGS
        - "Expense" maps to vn.EXPENSE
        - "Depreciation" maps to vn.DEPRECIATION
        - "OperatingIncome" maps to vn.OPERATING_INCOME
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the OperatingIncomeModel with standardized operational
        accounting boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration
                context dictionary.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_operating_income
        self._output_names = [vn.OPERATING_INCOME]

        # Revenue and core cost remain mandatory data inputs for processing
        self._required_variables = [
            vn.REVENUE,
            vn.COGS,
        ]

        # Shifted structural tracking lists into explicit dictionary default fallbacks
        self._optional_variables = {
            vn.EXPENSE: 0.0,
            vn.DEPRECIATION: 0.0,
        }
