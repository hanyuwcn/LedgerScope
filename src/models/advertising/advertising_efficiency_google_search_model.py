from src.config import variable_names
from src.core.base_model import Model


def calculate_leads_from_ads_budget_via_google_search(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates total prospect leads generated from specialized marketing channel investments.

    Mathematical Formula:
        Traffic (Clicks) = (AdsBudget * AllocationPercentage) / (CPC * USDToRMB)
        Leads = Traffic * ConversionRate

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing the required calculation
            metrics extracted from the model's global configuration variables:

            Mandatory Keys:
                COST_ADVERTISING (float): The total corporate multi-channel advertising budget.
                CPC_GOOGLE_SEARCH (float): Cost Per Click (CPC) explicitly for Google Search ads.
                CONVERSION_RATE_GOOGLE_SEARCH (float): Click-to-Lead configuration efficiency metric.

            Optional Keys:
                FINANCE_USD_TO_RMB (float, optional): Cross-border foreign currency multiplier.
                ALLOCATION_GOOGLE_SEARCH (float, optional): The fractional budget allocation percentage
                    devoted exclusively to Google Search campaigns.

    Returns:
        dict: A dictionary mapping the estimated lead acquisition volume to the centralized tracking registry.
            Example: {"Leads": 1420.5}
            Returns {"Leads": 0.0} if the denominator variables evaluate to zero to avoid runtime crashes.
    """
    ads_budget = kwargs[variable_names.COST_ADVERTISING]
    cpc = kwargs[variable_names.CPC_GOOGLE_SEARCH]
    conversion_rate = kwargs[variable_names.CONVERSION_RATE_GOOGLE_SEARCH]

    # Dynamically extract default value from the provided optional_variables structure
    default_usd_to_rmb = optional_variables[variable_names.FINANCE_USD_TO_RMB]
    usd_to_rmb = kwargs.get(variable_names.FINANCE_USD_TO_RMB, default_usd_to_rmb)

    default_google_search_allocation_percentage = optional_variables[variable_names.ALLOCATION_GOOGLE_SEARCH]
    google_search_allocation_percentage = kwargs.get(variable_names.ALLOCATION_GOOGLE_SEARCH,
                                                     default_google_search_allocation_percentage)

    # Protect calculation matrix from division by zero crashes
    denominator = cpc * usd_to_rmb
    if denominator == 0:
        return {variable_names.LEADS: 0.0}

    # Core operational funnel calculation with currency adjustments
    calculated_leads = (ads_budget * google_search_allocation_percentage * conversion_rate) / denominator

    return {variable_names.LEADS: calculated_leads}


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
        - "Budget" maps to COST_ADVERTISING
        - "Allocation" maps to ALLOCATION_GOOGLE_SEARCH
        - "CPC" maps to CPC_GOOGLE_SEARCH
        - "ExchangeRate" maps to FINANCE_USD_TO_RMB
        - "ConversionRate" maps to CONVERSION_RATE_GOOGLE_SEARCH
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the AdvertisingEfficiencyGoogleSearchModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary
                containing variables and metrics (e.g., {variable_names.COST_ADVERTISING: 2500}).
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        # Triggers parent to bind the input variable dictionary maps defensively
        super().__init__(input_variables)

        # Explicitly configure the execution bounds for this subclass pipeline step
        self._model_function = calculate_leads_from_ads_budget_via_google_search
        self._output_names = [variable_names.LEADS]

        self._required_variables = [
            variable_names.COST_ADVERTISING,
            variable_names.CPC_GOOGLE_SEARCH,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH,
        ]

        # Centralized mapping dictionary with 1.0 as the historical default state
        self._optional_variables = {
            variable_names.FINANCE_USD_TO_RMB: 1.0,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 1.0
        }