from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_return_on_advertising_spend(variables: dict) -> dict:
    """
    Calculates the Return on Advertising Spend (ROAS) metric for marketing
    performance tracking, with robust handling for zero-cost scenarios.

    Mathematical Formula:
        ROAS = Revenue / AdvertisingCost

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary containing the computed Return on Advertising Spend (ROAS),
            mapped directly to the global configuration constant name.
            Returns {"ROAS": 0.0} if advertising cost is zero to prevent division errors.
    """
    revenue = variables[vn.REVENUE]
    advertising_cost = variables[vn.ADVERTISING_COST]

    # Protect engine against a zero-denominator division crash
    if advertising_cost == 0:
        return {vn.ROAS: 0.0}

    calculated_roas = revenue / advertising_cost

    return {vn.ROAS: calculated_roas}


class RoasModel(Model):
    """
    Pipeline calculation block evaluating top-line capital returns against
    total marketing spend.

    Description:
        This model evaluates high-level marketing efficiency by mapping gross
        revenue output directly against top-of-funnel advertising expenditures.
        Under the current baseline assumption, all revenue is attributed to
        ad-driven performance channels. The model includes defensive guards
        to ensure pipeline stability during low-spend or zero-spend scenarios.

    Calculation Equation:
        ROAS = Revenue / AdvertisingCost

        Where:
        - "Revenue" maps to vn.REVENUE
        - "AdvertisingCost" maps to vn.ADVERTISING_COST
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the ReturnOnAdvertisingSpendModel with defined tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_return_on_advertising_spend
        self._output_names = [vn.ROAS]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.REVENUE,
            vn.ADVERTISING_COST
        ]
