from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_customer_acquisition_cost(variables: dict) -> dict:
    """
    Calculates the strategic Customer Acquisition Cost (CAC) for the operational cycle.

    Mathematical Formula:
        CAC = AdvertisingCost / Orders

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated customer acquisition cost
            to its central tracking constant.
            Returns {"CAC": 0.0} if zero orders are processed.
    """
    advertising_cost = variables[vn.ADVERTISING_COST]
    orders = variables[vn.ORDERS]

    # Protect engine against a zero-denominator division crash
    if orders == 0:
        return {vn.CAC: 0.0}

    calculated_cac = advertising_cost / orders

    return {vn.CAC: calculated_cac}


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
        - "AdvertisingCost" maps to vn.ADVERTISING_COST
        - "Orders" maps to vn.ORDERS
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
        self._output_names = [vn.CAC]

        # Explicit tracking validation boundaries (anchoring core inputs)
        self._required_variables = [
            vn.ADVERTISING_COST,
            vn.ORDERS
        ]
