from src.config import variable_names
from src.core.base_model import Model


def calculate_unit_free_on_board(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the point-of-origin Free On Board (FOB) wholesale unit value.

    This function isolates the gross intake price captured from downstream dealers or
    distributors after stripping out stacked supply chain leakages, ecosystem partner
    markups, or inbound shipping frictions from the final market retail configuration.

    Mathematical Formula:
        UnitFob = UnitRetail * (1 - DeductionRate)

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required mathematical inputs:

            Mandatory Keys:
                UNIT_RETAIL (float): The ultimate market price charged to end consumers.

            Optional Keys:
                DEDUCTION_RATE (float, optional): Aggregate friction multiplier modeling
                    the cumulative margin loss (e.g., Shipping + Channel Markup + Tariffs).
                    Defaults to 0.0 if not dynamically provided during execution cycles.

    Returns:
        dict: A single-element dictionary mapping the calculated point-of-origin port
            valuation to its designated registry signature.
            Example: {"UnitFob": 75.0}
    """
    unit_retail = kwargs[variable_names.UNIT_RETAIL]

    # Pull the baseline fallback rate from the parent model parameter mapping context
    default_deduction_rate = optional_variables[variable_names.DEDUCTION_RATE]
    deduction_rate = kwargs.get(variable_names.DEDUCTION_RATE, default_deduction_rate)

    unit_free_on_board = unit_retail * (1.0 - deduction_rate)

    return {variable_names.UNIT_FOB: unit_free_on_board}


class UnitFobModel(Model):
    """
    Pipeline calculation block responsible for transforming consumer-facing pricing
    structures into baseline B2B contractual port valuations.

    Description:
        This model functions as the primary top-down pricing waterfall block in the
        operational pipeline. By factoring cumulative leakage distributions directly
        against consumer shelf prices, it establishes a sanitized, normalized wholesale
        value. This metric directly serves as a prerequisite upstream dependencies hook
        for top-line revenue calculations.

    Calculation Equation:
        UnitFob = UnitRetail * (1 - DeductionRate)

        Where:
        - "UnitRetail" maps to variable_names.UNIT_RETAIL
        - "DeductionRate" maps to variable_names.DEDUCTION_RATE
        - "UnitFob" maps to variable_names.UNIT_FOB
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitFobModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding structural identities and specifying the explicit output registry signature
        self._model_function = calculate_unit_free_on_board
        self._output_names = [variable_names.UNIT_FOB]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            variable_names.UNIT_RETAIL
        ]

        # Transparently fallback to zero deduction to support isolated baseline simulations
        self._optional_variables = {
            variable_names.DEDUCTION_RATE: 0.0
        }
