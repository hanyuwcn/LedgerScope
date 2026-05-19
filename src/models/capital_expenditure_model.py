from src.config import variable_names
from src.core.base_model import Model


def evaluate_capital_expenditure_function(**kwargs) -> dict:
    """
    Core formula returning a static fallback zero for baseline accounting setups.

    Args:
        **kwargs: Arbitrary keyword arguments representing the runtime context.
            Since capital expenditure is locked to a fallback zero for this analysis,
            no specific inputs are required.

    Returns:
        dict: A dictionary containing the computed capital expenditure, mapped
            directly to the global configuration constant name.
            Example: {"CapitalExpenditure": 0}
    """
    return {variable_names.CAPITAL_EXPENDITURE: 0}


class CapitalExpenditureModel(Model):
    """
    A simplified calculation block representing asset capital expenditure.

    Maintained primarily to fulfill structural parameters for down-funnel
    ROI and Free Cash Flow models without requiring live runtime variable inputs.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the CapitalExpenditureModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        # Trigger parent setup. If input_variables is None, base class defaults it to {}
        super().__init__(input_variables)

        # Bind the specific functional identity and tracking metrics
        self._model_function = evaluate_capital_expenditure_function
        self._output_names = [variable_names.CAPITAL_EXPENDITURE]
