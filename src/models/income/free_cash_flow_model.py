from src.config import variable_names
from src.core.base_model import Model


def calculate_free_cash_flow(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates Unlevered Free Cash Flow (FCFF) to track true physical liquidity.

    Mathematical Formula:
        FreeCashFlow = NetIncome + Depreciation - CapitalExpenditure

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks
            for non-mandatory fields like DEPRECIATION and CAPITAL_EXPENDITURE.
        **kwargs: Arbitrary keyword arguments containing execution calculation metrics:

            Mandatory Keys:
                NET_INCOME (float): After-tax net profit pulled from the NetIncomeModel registry.

            Optional Keys (Defaults to configuration maps if missing):
                DEPRECIATION (float): Non-cash asset write-offs added back as a liquidity shield.
                CAPITAL_EXPENDITURE (float): Outbound cash investments spent maintaining or acquiring assets.

    Returns:
        dict: A dictionary mapping the final cash flow metric to the source-of-truth registry.
            Example: {"FreeCashFlow": 16500.0}
    """
    # Extract strictly required execution anchor
    net_income = kwargs[variable_names.NET_INCOME]

    # Resolve non-cash variables using runtime args, falling back securely to configuration defaults
    depreciation = kwargs.get(variable_names.DEPRECIATION, optional_variables.get(variable_names.DEPRECIATION))
    cap_ex = kwargs.get(variable_names.CAPITAL_EXPENDITURE, optional_variables.get(variable_names.CAPITAL_EXPENDITURE))

    # Reconciling accounting profits back to true liquid asset flows
    calculated_fcf = net_income + depreciation - cap_ex

    return {variable_names.FREE_CASH_FLOW: calculated_fcf}


class FreeCashFlowModel(Model):
    """
    Pipeline calculation block evaluating corporate liquidity by reconciling non-cash
    depreciation write-offs and subtracting asset adjustments from net earnings.

    In a Nutshell:
        Free Cash Flow (FCF) is the actual, spendable cash a business generates after
        paying for its daily operations and maintaining its physical assets. While accounting
        metrics like "Net Income" include non-cash paper adjustments (like depreciation) and
        ignore raw equipment spending, FCF cuts through the accounting fluff to show the
        real liquid cash available to pay back debt, distribute to investors, or reinvest
        into growth.

    Description:
        The Free Cash Flow Model serves as the ultimate reality check for business viability within
        the pipeline. A company can show strong paper profitability under a Net Income lens while
        simultaneously starving for cash due to heavy capital investment requirements.

        By re-injecting non-cash depreciation back into net earnings and extracting immediate
        capital expenditures (CapEx), this model helps analysts evaluate the pure organic liquidity
        engine of the target business.

        To maximize flexibility across early-stage or service-oriented business profiles,
        depreciation and capital expenditures are treated as optional parameters, defaulting
        safely to 0.0 if the business model does not maintain heavy asset footprints.

    Calculation Equation:
        free_cash_flow = net_income + depreciation - capital_expenditure

        Where:
        - "net_income" maps to NET_INCOME (Required)
        - "depreciation" maps to DEPRECIATION (Optional, Default: 0.0)
        - "capital_expenditure" maps to CAPITAL_EXPENDITURE (Optional, Default: 0.0)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the FreeCashFlowModel with standardized system boundaries and fallback maps.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_free_cash_flow
        self._output_names = [variable_names.FREE_CASH_FLOW]

        # Explicit tracking validation boundaries
        self._required_variables = [
            variable_names.NET_INCOME
        ]

        # Establishing safe pipeline fallbacks for asset-light configurations
        self._optional_variables = {
            variable_names.DEPRECIATION: 0.0,
            variable_names.CAPITAL_EXPENDITURE: 0.0
        }
