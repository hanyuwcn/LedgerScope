from src.config import variable_names
from src.core.base_model import Model


def evaluate_capital_expenditure_function(optional_variables: dict, **kwargs) -> dict:
    """
    Core formula returning a static fallback zero for baseline accounting setups.

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments representing the runtime context.
            Since capital expenditure is locked to a fallback zero for this analysis,
            no specific inputs are required.

    Returns:
        dict: A dictionary containing the computed capital expenditure, mapped
            directly to the global configuration constant name.
            Example: {"CapitalExpenditure": 0.0}
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
    Pipeline calculation block representing corporate capital expenditure (CapEx).

    Description:
        Capital Expenditure (CapEx) represents the funds a business uses to acquire, upgrade,
        and maintain physical assets such as property, plants, buildings, technology, or equipment.
        Unlike operational expenses (OpEx), which cover day-to-day running costs, CapEx is an investment
        in long-term structural infrastructure designed to scale business capacity or prolong
        asset lifespans.

        Right now, this business layer registers no active capital investments. Consequently, this model
        is hardcoded to evaluate to 0.0. Maintaining this placeholder structure isolates the financial pipeline
        and satisfies upstream contract dependencies for complex down-funnel models like Return on Investment (ROI)
        and Free Cash Flow (FCF) calculations.
    """
        # Trigger parent setup. If input_variables is None, base class defaults it to {}
        super().__init__(input_variables)

        # Bind the specific functional identity and tracking metrics
        self._model_function = evaluate_capital_expenditure_function
        self._output_names = [variable_names.CAPITAL_EXPENDITURE]
