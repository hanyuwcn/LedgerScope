from src.config import variable_names
from src.core.base_model import Model


def calculate_unit_contribution_margin(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the marginal profit contribution of each individual unit sold.

    Mathematical Formula:
        Unit Contribution Margin = Profit / (Orders * ItemsPerOrder)

    Description:
        This function normalizes the total realized profit across the absolute volume of units
        shipped. By multiplying 'Orders' by 'ItemsPerOrder', it establishes the total unit
        denominator required to identify the per-item surplus available to cover fixed
        costs or contribute to net earnings.

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                PROFIT (float): The net earnings or surplus generated in the current cycle.
                DEAL_ORDERS (int or float): The total count of converted sales transactions.
                DEAL_ITEMS_PER_ORDER (int or float): The average quantity of units per transaction.

    Returns:
        dict: A dictionary mapping the unit contribution margin to its central tracking constant.
            Example: {"UnitContributionMargin": 4.25}
            Safely returns {"UnitContributionMargin": 0.0} if the total unit volume is zero.
    """
    # Extract strictly required execution anchors
    profit = kwargs[variable_names.PROFIT]
    orders = kwargs[variable_names.DEAL_ORDERS]
    items_per_order = kwargs[variable_names.DEAL_ITEMS_PER_ORDER]

    total_unit_volume = orders * items_per_order

    # Protect engine against a zero-denominator division crash
    if total_unit_volume == 0:
        return {variable_names.UNIT_CONTRIBUTION_MARGIN: 0.0}

    calculated_unit_contribution_margin = profit / total_unit_volume

    return {variable_names.UNIT_CONTRIBUTION_MARGIN: calculated_unit_contribution_margin}


class UnitContributionMarginModel(Model):
    """
    Pipeline calculation block responsible for quantifying unit-level profitability
    by determining the Unit Contribution Margin (UCM).

    Description:
        The Unit Contribution Margin is a fundamental indicator of operational leverage.
        This model isolates the profit performance of a single unit of inventory, allowing
        for precise break-even analysis and product-mix optimization. It helps in
        understanding how much of each unit's price remains to cover foundational overhead
        after all variable expenses are accounted for.

    Calculation Equation:
        unit contribution margin = profit / (total converted orders * items per order)

        Where:
        - "profit" maps to PROFIT
        - "total converted orders" maps to DEAL_ORDERS
        - "items per order" maps to DEAL_ITEMS_PER_ORDER
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitContributionMarginModel with explicit validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_unit_contribution_margin
        self._output_names = [variable_names.UNIT_CONTRIBUTION_MARGIN]

        # Explicit tracking validation boundaries (anchoring core inputs)
        self._required_variables = [
            variable_names.PROFIT,
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_ITEMS_PER_ORDER
        ]