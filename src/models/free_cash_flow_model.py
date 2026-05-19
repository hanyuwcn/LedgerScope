from src.config import variable_names
from src.core.base_model import Model


def calculate_free_cash_flow(**kwargs) -> dict:
    """
    Calculates Unlevered Free Cash Flow (FCFF) to track physical liquidity.

    Mathematical Formula:
        FreeCashFlow = NetIncome + Depreciation - CapitalExpenditure

    Args:
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                NET_INCOME (float): After-tax net profit from NetIncomeModel.
                DEPRECIATION (float): Non-cash asset write-offs added back as a tax shield.
                CAPITAL_EXPENDITURE (float): Outbound cash investments spent acquiring physical assets.

    Returns:
        dict: A dictionary mapping the final cash flow metric to the source-of-truth registry.
            Example: {"FreeCashFlow": 16500.0}
    """
    net_income = kwargs[variable_names.NET_INCOME]
    depreciation = kwargs[variable_names.DEPRECIATION]
    cap_ex = kwargs[variable_names.CAPITAL_EXPENDITURE]

    # Reconciling accounting profits back to true liquid asset flows
    calculated_fcf = net_income + depreciation - cap_ex

    return {variable_names.FREE_CASH_FLOW: calculated_fcf}


class FreeCashFlowModel(Model):
    """
    Pipeline calculation block evaluating corporate liquidity by reconciling non-cash
    depreciation write-offs and subtracting asset adjustments from net earnings.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the FreeCashFlowModel with standardized system boundaries.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_free_cash_flow
        self._output_names = [variable_names.FREE_CASH_FLOW]

        # Explicit tracking requirements
        self._required_variables = [
            variable_names.NET_INCOME,
            variable_names.DEPRECIATION,
            variable_names.CAPITAL_EXPENDITURE
        ]
