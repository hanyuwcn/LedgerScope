from src.config import variable_names
from src.core.base_model import Model


def calculate_cost_per_lead_in_google_search(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the Cost Per Lead (CPL) for marketing traffic routed through Google Search.

    Mathematical Formula:
        CPL = ads_budget ÷ ((ads_budget × action_percentage ÷ (CPC * USDToRMB)) × CVR)
            = (CPC * USDToRMB) / (ConversionRate * AllocationPercentage)

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing the required calculation
            metrics extracted from the model's global configuration variables.

            Mandatory Keys:
                CPC_GOOGLE_SEARCH (float): Cost Per Click specifically for Google Search ads.
                CONVERSION_RATE_GOOGLE_SEARCH (float): Clicks-to-leads conversion rate.

            Optional Keys:
                FINANCE_USD_TO_RMB (float, optional): Cross-border currency multiplier.
                ALLOCATION_GOOGLE_SEARCH (float, optional): The fractional allocation percentage
                    of total ads budget devoted exclusively to Google Search campaigns.

    Returns:
        dict: A dictionary containing the computed Cost Per Lead (CPL) metric,
            mapped directly to the global configuration constant name.
            Example: {"CPLGoogleSearch": 62.50}
    """
    cpc = kwargs[variable_names.CPC_GOOGLE_SEARCH]
    conversion_rate = kwargs[variable_names.CONVERSION_RATE_GOOGLE_SEARCH]

    # Dynamically extract default value from the provided optional_variables structure
    default_usd_to_rmb = optional_variables[variable_names.FINANCE_USD_TO_RMB]
    usd_to_rmb = kwargs.get(variable_names.FINANCE_USD_TO_RMB, default_usd_to_rmb)

    default_google_search_allocation_percentage = optional_variables[variable_names.ALLOCATION_GOOGLE_SEARCH]
    google_search_allocation_percentage = kwargs.get(variable_names.ALLOCATION_GOOGLE_SEARCH,
                                                     default_google_search_allocation_percentage)

    # Core operational calculation scaled to target currency
    cost_per_leads = (cpc * usd_to_rmb) / (conversion_rate * google_search_allocation_percentage)

    return {variable_names.CPL_GOOGLE_SEARCH: cost_per_leads}


class CostPerLeadGoogleSearchModel(Model):
    """
    Pipeline calculation block evaluating traffic cost dynamics to isolate Google Search CPL.

    Description:
        This model isolates top-of-funnel conversion costs by evaluating Cost Per Click (CPC)
        against traffic-to-lead conversion efficiency and specific campaign budget distributions.
        The resulting metric isolates the financial efficiency of raw lead acquisition before
        those contacts move downstream to undergo Marketing Qualified Lead (MQL) or Sales Qualified
        Lead (SQL) grading structures.

    Calculation Equation:
        CPL = (CPC * ExchangeRate) / (ConversionRate * Allocation)

        Where:
        - "CPC" maps to CPC_GOOGLE_SEARCH
        - "ExchangeRate" maps to FINANCE_USD_TO_RMB
        - "ConversionRate" maps to CONVERSION_RATE_GOOGLE_SEARCH
        - "Allocation" maps to ALLOCATION_GOOGLE_SEARCH
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the CostPerLeadGoogleSearchModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary
                containing variables and metrics (e.g., {variable_names.CPC_GOOGLE_SEARCH: 2.50}).
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        # Triggers parent to bind the input variable dictionary maps defensively
        super().__init__(input_variables)

        # Hooking calculation logic and specifying the correct output variable
        self._model_function = calculate_cost_per_lead_in_google_search
        self._output_names = [variable_names.CPL_GOOGLE_SEARCH]

        self._required_variables = [
            variable_names.CPC_GOOGLE_SEARCH,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH,
        ]

        # Centralized mapping dictionary with 1.0 as the historical default state
        self._optional_variables = {
            variable_names.FINANCE_USD_TO_RMB: 1.0,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 1.0
        }