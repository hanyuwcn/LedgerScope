from src.config import variable_names
from src.core.base_model import Model


def evaluate_depreciation_function(**kwargs) -> dict:
    """Core formula returning a static fallback zero for baseline accounting setups."""
    return {variable_names.DEPRECIATION: 0}


class DepreciationModel(Model):
    """
    A simplified calculation block representing asset depreciation.

    Maintained primarily to fulfill structural parameters for down-funnel 
    ROI and Free Cash Flow models without requiring live runtime variable inputs.
    """

    def __init__(self, input_variables: dict = None):
        # Trigger parent setup. If input_variables is None, base class defaults it to {}
        super().__init__(input_variables)

        # Bind the specific functional identity and tracking metrics
        self._model_function = evaluate_depreciation_function
        self._output_names = [variable_names.DEPRECIATION]
