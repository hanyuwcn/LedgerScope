from src.config import variable_names
from src.core.base_model import Model


def calculate_cost_per_lead_in_google_search(variables: dict) -> dict:
    """
    Calculates the blended Cost Per Lead (CPL) relative to total multi-channel ad spend.

    Mathematical Formula:
        CPL = CPC / (ConversionRate * AllocationPercentage)

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary containing the computed blended Cost Per Lead (CPL) metric.
            Returns {"CPL_GOOGLE_SEARCH": 0.0} if the denominator evaluates to zero.
    """
    cpc = variables[variable_names.CPC_GOOGLE_SEARCH]
    conversion_rate = variables[variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
    allocation = variables[variable_names.ALLOCATION_GOOGLE_SEARCH]

    # Protect calculation matrix from division by zero crashes
    denominator = conversion_rate * allocation
    if denominator == 0:
        return {variable_names.CPL_GOOGLE_SEARCH: 0.0}

    # Core operational calculation
    cost_per_lead = cpc / denominator

    return {variable_names.CPL_GOOGLE_SEARCH: cost_per_lead}


class CostPerLeadGoogleSearchModel(Model):
    """
    Pipeline calculation block evaluating cross-channel cost dynamics to isolate
    blended Google Search CPL against total budget footprints.

    Description:
        This model isolates top-of-funnel conversion costs by evaluating Cost Per Click (CPC)
        against traffic-to-lead conversion efficiency and specific campaign budget distributions.
        The resulting metric isolates the financial efficiency of lead acquisition relative to
        total multi-channel outlays natively evaluated in USD.

    Calculation Equation:
        CPL = CPC / (ConversionRate * Allocation)

        Where:
        - "CPC" maps to CPC_GOOGLE_SEARCH
        - "ConversionRate" maps to CONVERSION_RATE_GOOGLE_SEARCH
        - "Allocation" maps to ALLOCATION_GOOGLE_SEARCH
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the CostPerLeadGoogleSearchModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
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
            variable_names.ALLOCATION_GOOGLE_SEARCH: 1.0
        }
