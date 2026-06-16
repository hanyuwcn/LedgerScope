from src.config import variable_names as vn
from src.core.base_model import Model


## TODO: AdvertisingExpense can be convert to USD here
def calculate_advertising_expense(variables: dict) -> dict:
    """
    Calculates the advertising expense by allocating the total marketing
    budget to advertising.

    Mathematical Formula:
        AdvertisingExpense = MarketingExpense * 1.0

    Args:
        variables (dict): Unified context containing the marketing expense.

    Returns:
        dict: A dictionary mapping the calculated advertising expense to
            the pipeline registry.
    """
    marketing_expense = variables[vn.MARKETING_EXPENSE]

    # Allocation logic: 100% of marketing spend is directed to advertising
    advertising_expense = marketing_expense * 1.0
    return {vn.ADVERTISING_EXPENSE: advertising_expense}


class AdvertisingExpenseModel(Model):
    """
    Pipeline calculation block responsible for allocating the marketing budget
    to advertising activities.

    Description:
        This model facilitates the translation of top-level marketing expenditure
        into specific advertising costs. Currently, it assumes a full-allocation
        model where the entire marketing budget is treated as advertising spend.

    Calculation Equation:
        AdvertisingExpense = MarketingExpense * 1.0

        Where:
        - "MarketingExpense" maps to vn.MARKETING_EXPENSE (Required)
        - "AdvertisingExpense" maps to vn.ADVERTISING_EXPENSE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the AdvertisingExpenseModel with mandatory marketing inputs.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_advertising_expense
        self._output_names = [vn.ADVERTISING_EXPENSE]

        # Marketing expense is the mandatory prerequisite
        self._required_variables = [
            vn.MARKETING_EXPENSE,
        ]

        self._optional_variables = {}
