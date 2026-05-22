from src.config import variable_names
from src.core.base_model import Model


def calculate_order_from_ads_budget(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates total transactional orders generated from marketing spend metrics.

    Mathematical Formula:
        Orders = (AdvertisingCost * ConversionRate) / (CostPerAcquisition * USDToRMB)

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing the required calculation
            metrics extracted from the model's global configuration variables.

            Mandatory Keys:
                COST_ADVERTISING (float): The total budget allocated to advertising campaigns.
                COST_CONVERSION_RATE (float): The fractional conversion rate of traffic to
                    actions (e.g., 0.05 for 5%).
                COST_CPA (float): Cost Per Acquisition metric defining the cost threshold
                    per successful conversion.

            Optional Keys:
                FINANCE_USD_TO_RMB (float, optional): Cross-border currency multiplier.
                    Used if advertising costs and acquisition fees are denominated across
                    different international currencies.

    Returns:
        dict: A dictionary containing the computed volume of transaction orders,
            mapped directly to the global configuration constant name.
            Example: {"Orders": 35.71}
    """
    cost_ads = kwargs[variable_names.COST_ADVERTISING]
    conversion_rate = kwargs[variable_names.COST_CONVERSION_RATE]
    cpa = kwargs[variable_names.COST_CPA]

    # Dynamically extract default value from the provided optional_variables structure
    default_usd_to_rmb = optional_variables[variable_names.FINANCE_USD_TO_RMB]
    usd_to_rmb = kwargs.get(variable_names.FINANCE_USD_TO_RMB, default_usd_to_rmb)

    # Core operational calculation
    calculated_orders = (cost_ads * conversion_rate) / (cpa * usd_to_rmb)

    return {variable_names.DEAL_ORDERS: calculated_orders}


class AdvertisingEfficiencyModel(Model):
    """
    Pipeline calculation block evaluating marketing acquisition spend to project total orders.

    Description:
        This model processes corporate marketing expenditures and returns projected unit sale
        volumes based on digital campaign conversion rates and acquisition pricing constraints.
        It isolates structural efficiency before feeding operational values to down-stream
        revenue or financial mapping pipelines.

    Calculation Equation:
        Orders to get from Ads = Budget from Advertising * Conversion rate / (Currency exchange rate * Effective Ads per cost)

        Where:
        - "Budget from Advertising" maps to COST_ADVERTISING
        - "Conversion rate" maps to COST_CONVERSION_RATE
        - "Currency exchange rate" maps to FINANCE_USD_TO_RMB
        - "Effective Ads per cost" maps to COST_CPA
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the AdvertisingEfficiencyModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary
                containing variables and metrics (e.g., {variable_names.COST_ADVERTISING: 5000}).
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        # Triggers parent to bind the input variable dictionary maps defensively
        super().__init__(input_variables)

        # Explicitly configure the execution bounds for this subclass pipeline step
        self._model_function = calculate_order_from_ads_budget
        self._output_names = [variable_names.DEAL_ORDERS]

        self._required_variables = [
            variable_names.COST_ADVERTISING,
            variable_names.COST_CONVERSION_RATE,
            variable_names.COST_CPA
        ]

        # Centralized mapping dictionary with 1.0 as the historical default state
        self._optional_variables = {
            variable_names.FINANCE_USD_TO_RMB: 1.0
        }
