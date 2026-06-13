from src.config import variable_names
from src.core.base_model import Model


def evaluate_depreciation_function(variables: dict) -> dict:
    """
    Core formula returning a static fallback zero for baseline accounting setups.

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary containing the computed depreciation value, mapped
            directly to the global configuration constant name.
            Example: {"DEPRECIATION": 0.0}
    """
    return {variable_names.DEPRECIATION: 0}


class DepreciationModel(Model):
    """
    Pipeline calculation block representing fixed asset depreciation.

    Description:
        Depreciation is the systematic, non-cash accounting method used to allocate the cost of
        a tangible asset over its useful lifespan. It reflects how much of an asset's value has
        been consumed or worn out over time (e.g., computers, vehicles, or machinery losing value).
        While it is a non-cash expense, accounting for depreciation is vital for accurately tracking
        tax liabilities and net operating income.

        For the time being, this model is configured to return a baseline of 0.0, as there are no
        depreciable corporate assets actively tracked in the current cycle. Preserving this
        placeholder structure prevents pipeline breaks and fulfills contract signatures for upstream,
        down-funnel financial blocks like Net Profit, ROI, and Free Cash Flow (FCF) metrics.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the DepreciationModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        # Trigger parent setup. If input_variables is None, base class defaults it to {}
        super().__init__(input_variables)

        # Bind the specific functional identity and tracking metrics
        self._model_function = evaluate_depreciation_function
        self._output_names = [variable_names.DEPRECIATION]
