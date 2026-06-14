from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_free_on_board(variables: dict) -> dict:
    """
    Calculates the point-of-origin Free On Board (FOB) wholesale unit value.

    Mathematical Formula:
        UnitFob = UnitRetail * (1 - DeductionRate)

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the calculated point-of-origin
            port valuation to its designated registry signature.
            Example: {"UNIT_FOB": 75.0}
    """
    unit_retail = variables[vn.UNIT_RETAIL]
    deduction_rate = variables[vn.DEDUCTION_RATE]

    unit_free_on_board = unit_retail * (1.0 - deduction_rate)

    return {vn.UNIT_FOB: unit_free_on_board}


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
        - "UnitRetail" maps to vn.UNIT_RETAIL
        - "DeductionRate" maps to vn.DEDUCTION_RATE
        - "UnitFob" maps to vn.UNIT_FOB
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
        self._output_names = [vn.UNIT_FOB]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.UNIT_RETAIL
        ]

        # Transparently fallback to zero deduction to support isolated baseline simulations
        self._optional_variables = {
            vn.DEDUCTION_RATE: 0.0
        }
