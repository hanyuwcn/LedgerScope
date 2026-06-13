from src.config import variable_names
from src.core.base_model import Model


def calculate_deduction_rate(variables: dict) -> dict:
    """
    Calculates the aggregate gross margin deduction rate leakage coefficient.

    Mathematical Formula:
        DeductionRate = ShippingRate + TariffRate + ChannelMarkupRate

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the calculated combined leak coefficient
            to its master registry key signature.
            Example: {"DEDUCTION_RATE": 0.43}
    """
    shipping_rate = variables[variable_names.SHIPPING_RATE]
    tariff_rate = variables[variable_names.TARIFF_RATE]
    channel_markup_rate = variables[variable_names.CHANNEL_MARKUP_RATE]

    # Accumulate stacked percentage leaks
    deduction_rate = shipping_rate + tariff_rate + channel_markup_rate

    return {variable_names.DEDUCTION_RATE: deduction_rate}


class DeductionRateModel(Model):
    """
    Pipeline calculation block responsible for building the cumulative top-down
    pricing waterfall deduction baseline.

    Description:
        This model functions as an architectural aggregator node. It consolidates independent
        logistical, fiscal, and commercial percentage losses into a single systemic cost leak.
        This consolidated index serves as a direct input dependency hook for downstream port
        valuation blocks (such as UnitFobModel).

    Calculation Equation:
        DeductionRate = ShippingRate + TariffRate + ChannelMarkupRate

        Where:
        - "ShippingRate" maps to variable_names.SHIPPING_RATE
        - "TariffRate" maps to variable_names.TARIFF_RATE
        - "ChannelMarkupRate" maps to variable_names.CHANNEL_MARKUP_RATE
        - "DeductionRate" maps to variable_names.DEDUCTION_RATE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the DeductionRateModel with explicit fallback tracking boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional pointer logic and mapping outputs to the central registry
        self._model_function = calculate_deduction_rate
        self._output_names = [variable_names.DEDUCTION_RATE]

        # Establishing required variables (all metrics default to optional to support flexible baseline runs)
        self._required_variables = [
        ]

        # Migrated from standard list footprint to map defaults transparently to 0.0
        self._optional_variables = {
            variable_names.SHIPPING_RATE: 0.0,
            variable_names.TARIFF_RATE: 0.0,
            variable_names.CHANNEL_MARKUP_RATE: 0.0
        }
