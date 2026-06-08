from src.config import variable_names
from src.core.base_model import Model


def calculate_customer_acquisition_cost(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the strategic Customer Acquisition Cost (CAC) for the operational cycle.

    Mathematical Formula:
        CAC = AdvertisingCost / Orders

    Note:
        The structural formula design supports downstream expansion to include variable
        affiliate or sales commissions: (AdvertisingCost + (Revenue * CommissionRate)) / Orders.
        The commission components are intentionally ignored in the current iteration.

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                ADVERTISING_COST (float): Total budget allocated toward marketing and acquisition channels.
                ORDERS (int or float): Total volume of converted customer purchase orders.

    Returns:
        dict: A dictionary mapping the calculated customer acquisition cost to its central tracking constant.
            Example: {"CAC": 15.50}
            Safely returns {"CAC": 0.0} if zero orders are processed to bypass division errors.
    """
    # Extract strictly required execution anchors
    advertising_cost = kwargs[variable_names.ADVERTISING_COST]
    orders = kwargs[variable_names.ORDERS]

    # Protect engine against a zero-denominator division crash
    if orders == 0:
        return {variable_names.CAC: 0.0}

    calculated_cac = advertising_cost / orders

    return {variable_names.CAC: calculated_cac}


class CacModel(Model):
    """
    Pipeline calculation block responsible for evaluation of marketing capital efficiency
    by profiling unit-level Customer Acquisition Costs (CAC).

    Description:
        This model serves as a core diagnostic anchor for unit economics. By normalizing aggregate
        marketing outlays against total realized conversions over a given cycle, it quantifies the
        direct capital required to win a single purchasing customer. This metric is fundamentally
        critical for evaluating lifetime value (LTV) ratios and marketing scalability.

    Calculation Equation:
        CAC = AdvertisingCost / Orders

        Where:
        - "AdvertisingCost" maps to variable_names.ADVERTISING_COST
        - "Orders" maps to variable_names.ORDERS
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the CACModel with explicit validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_customer_acquisition_cost
        self._output_names = [variable_names.CAC]

        # Explicit tracking validation boundaries (anchoring core inputs)
        self._required_variables = [
            variable_names.ADVERTISING_COST,
            variable_names.ORDERS
        ]
