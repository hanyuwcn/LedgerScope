from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_contribution_margin(variables: dict) -> dict:
    """
    Calculates the marginal profit contribution of each individual unit sold.

    Mathematical Formula:
        Unit Contribution Margin = Profit / (Orders * UnitsPerOrder)

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the unit contribution margin to its
            central tracking constant.
            Returns {"UNIT_CONTRIBUTION_MARGIN": 0.0} if the total unit
            volume is zero to prevent division by zero.
    """
    profit = variables[vn.PROFIT]
    orders = variables[vn.ORDERS]
    items_per_order = variables[vn.UNITS_PER_ORDER]

    total_unit_volume = orders * items_per_order

    # Protect engine against a zero-denominator division crash
    if total_unit_volume == 0:
        return {vn.UNIT_CONTRIBUTION_MARGIN: 0.0}

    calculated_unit_contribution_margin = profit / total_unit_volume

    return {vn.UNIT_CONTRIBUTION_MARGIN: calculated_unit_contribution_margin}


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
        UnitContributionMargin = Profit / (Orders * UnitsPerOrder)

        Where:
        - "Profit" maps to vn.PROFIT
        - "Orders" maps to vn.ORDERS
        - "UnitsPerOrder" maps to vn.UNITS_PER_ORDER
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
        self._output_names = [vn.UNIT_CONTRIBUTION_MARGIN]

        # Explicit tracking validation boundaries (anchoring core inputs)
        self._required_variables = [
            vn.PROFIT,
            vn.ORDERS,
            vn.UNITS_PER_ORDER
        ]
