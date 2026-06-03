from src.config import variable_names
from src.core.base_model import Model


def calculate_order_from_ads_budget_via_google_search(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates total transactional orders generated from marketing spend metrics.

    Mathematical Formula:
        Orders = ((AdsBudget * AllocationPercentage) / (CPC * USDToRMB)) * ConversionRate * CloseRate

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing the required calculation
            metrics extracted from the model's global configuration variables.

            Mandatory Keys:
                COST_ADVERTISING (float): The total corporate advertising budget.
                CPC_GOOGLE_SEARCH (float): Cost Per Click specifically for Google Search ads.
                CONVERSION_RATE_GOOGLE_SEARCH (float): Clicks-to-leads efficiency metric.
                CLOSE_RATE (float): Leads-to-orders closed sales efficiency metric.

            Optional Keys:
                FINANCE_USD_TO_RMB (float, optional): Cross-border currency multiplier.
                ALLOCATION_GOOGLE_SEARCH (float, optional): The fractional allocation percentage
                    of total ads budget devoted exclusively to Google Search campaigns.

    Returns:
        dict: A dictionary containing the computed volume of transaction orders,
            mapped directly to the global configuration constant name.
            Example: {"Orders": 42.50}
    """
    ads_budget = kwargs[variable_names.COST_ADVERTISING]
    cpc = kwargs[variable_names.CPC_GOOGLE_SEARCH]
    conversion_rate = kwargs[variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
    close_rate = kwargs[variable_names.CLOSE_RATE]

    # Dynamically extract default value from the provided optional_variables structure
    default_usd_to_rmb = optional_variables[variable_names.FINANCE_USD_TO_RMB]
    usd_to_rmb = kwargs.get(variable_names.FINANCE_USD_TO_RMB, default_usd_to_rmb)

    default_google_search_allocation_percentage = optional_variables[variable_names.ALLOCATION_GOOGLE_SEARCH]
    google_search_allocation_percentage = kwargs.get(variable_names.ALLOCATION_GOOGLE_SEARCH,
                                                     default_google_search_allocation_percentage)

    # Core operational funnel calculation with currency adjustments
    calculated_orders = (ads_budget * google_search_allocation_percentage * conversion_rate * close_rate) / (cpc * usd_to_rmb)

    return {variable_names.DEAL_ORDERS: calculated_orders}


class AdvertisingEfficiencyGoogleSearchModel(Model):
    """
    Pipeline calculation block evaluating marketing acquisition spend to project total orders
    through the Google Search channel.

    Description:
        This model processes corporate marketing budget investments and models execution metrics
        sequentially across the customer acquisition funnel—handling traffic acquisition cost,
        digital lead capture efficiency, and localized sales conversion rates. It separates channel
        allocation dynamics before passing transactional outputs down to inventory or ledger revenue systems.

    Calculation Equation:
        Orders = ((Budget * Allocation) / (CPC * ExchangeRate)) * ConversionRate * CloseRate

        Where:
        - "Budget" maps to COST_ADVERTISING
        - "Allocation" maps to ALLOCATION_GOOGLE_SEARCH
        - "CPC" maps to CPC_GOOGLE_SEARCH
        - "ExchangeRate" maps to FINANCE_USD_TO_RMB
        - "ConversionRate" maps to CONVERSION_RATE_GOOGLE_SEARCH
        - "CloseRate" maps to CLOSE_RATE
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
        self._model_function = calculate_order_from_ads_budget_via_google_search
        self._output_names = [variable_names.DEAL_ORDERS]

        self._required_variables = [
            variable_names.COST_ADVERTISING,
            variable_names.CPC_GOOGLE_SEARCH,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH,
            variable_names.CLOSE_RATE
        ]

        # Centralized mapping dictionary with 1.0 as the historical default state
        self._optional_variables = {
            variable_names.FINANCE_USD_TO_RMB: 1.0,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 1.0
        }