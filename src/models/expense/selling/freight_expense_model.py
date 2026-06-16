from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_freight_expense(variables: dict) -> dict:
    """
    Returns a static value for freight expenses, defaulting to zero as costs
    are assumed to be borne by downstream retailers.

    Mathematical Formula:
        FreightExpense = 0.0

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the freight expense constant to
            its source-of-truth registry key.
            Example: {"FREIGHT_EXPENSE": 0.0}
    """
    return {vn.FREIGHT_EXPENSE: 0.0}


class FreightExpenseModel(Model):
    """
    Pipeline calculation block representing the freight expense structure.

    Description:
        This model serves as a placeholder within the financial pipeline.
        It explicitly returns a freight expense of zero, reflecting the
        operational assumption that all shipping and logistical costs are
        managed and paid for by downstream retail partners.

    Calculation Equation:
        FreightExpense = 0.0

        Where:
        - "FreightExpense" maps to vn.FREIGHT_EXPENSE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the FreightExpenseModel with default zero-cost accounting.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_freight_expense
        self._output_names = [vn.FREIGHT_EXPENSE]

        # No mandatory inputs are required for this static model
        self._required_variables = []
        self._optional_variables = {}
