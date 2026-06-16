from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_leads_from_ads_budget_via_google_search(variables: dict) -> dict:
    """
    Calculates total prospect leads generated from specialized marketing channel investments.

    Mathematical Formula:
        Traffic = (Budget * Allocation) / (CPC * USDToRMB)
        Leads = Traffic * ConversionRate

    Args:
        variables (dict): Unified context containing all mandatory and optional variables.

    Returns:
        dict: Mapping of estimated lead acquisition volume to the centralized registry.
    """
    ads_budget = variables[vn.ADVERTISING_EXPENSE]
    cpc = variables[vn.CPC_GOOGLE_SEARCH]
    conversion_rate = variables[vn.CONVERSION_RATE_GOOGLE_SEARCH]
    usd_to_rmb = variables[vn.USD_TO_RMB]
    allocation = variables[vn.ALLOCATION_GOOGLE_SEARCH]

    # Protect calculation matrix from division by zero
    denominator = cpc * usd_to_rmb
    if denominator == 0:
        return {vn.LEADS: 0.0}

    # Core operational funnel calculation
    calculated_leads = (ads_budget * allocation * conversion_rate) / denominator

    return {vn.LEADS: calculated_leads}


class AdvertisingEfficiencyGoogleSearchModel(Model):
    """
    Pipeline calculation block evaluating ad budget deployment efficiency to project
    top-of-funnel prospect Leads generated through the Google Search channel.

    Description:
        This model processes overall corporate marketing budget investments, narrows down
        the specific channel allocation capital, and applies cost-per-click and click-to-lead
        conversion mechanics. By terminating its calculation step at raw acquired leads,
        it allows for down-funnel downstream separation of lead nurturing and order-closing processes.

    Calculation Equation:
        Leads = ((Budget * Allocation) / (CPC * ExchangeRate)) * ConversionRate

        Where:
        - "Budget" maps to vn.ADVERTISING_COST
        - "Allocation" maps to vn.ALLOCATION_GOOGLE_SEARCH
        - "CPC" maps to vn.CPC_GOOGLE_SEARCH
        - "ExchangeRate" maps to vn.USD_TO_RMB
        - "ConversionRate" maps to vn.CONVERSION_RATE_GOOGLE_SEARCH
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the AdvertisingEfficiencyGoogleSearchModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary
                containing variables and metrics (e.g., {vn.ADVERTISING_COST: 2500}).
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        # Triggers parent to bind the input variable dictionary maps defensively
        super().__init__(input_variables)

        # Explicitly configure the execution bounds for this subclass pipeline step
        self._model_function = calculate_leads_from_ads_budget_via_google_search
        self._output_names = [vn.LEADS]

        self._required_variables = [
            vn.ADVERTISING_EXPENSE,
            vn.CPC_GOOGLE_SEARCH,
            vn.CONVERSION_RATE_GOOGLE_SEARCH,
        ]

        # Centralized mapping dictionary with 1.0 as the historical default state
        self._optional_variables = {
            vn.USD_TO_RMB: 1.0,
            vn.ALLOCATION_GOOGLE_SEARCH: 1.0
        }
