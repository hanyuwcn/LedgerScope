from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_deduction_rate(variables: dict) -> dict:
    """
    Calculates the aggregate gross margin deduction rate leakage coefficient.

    Mathematical Formula:
        DeductionRate = MerchantFreightRate + TariffRate + ChannelMarkupRate

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the calculated combined leak coefficient
            to its master registry key signature.
            Example: {"DeductionRate": 0.43}
    """
    freight_rate = variables[vn.MERCHANT_FREIGHT_RATE]
    tariff_rate = variables[vn.TARIFF_RATE]
    channel_markup_rate = variables[vn.CHANNEL_MARKUP_RATE]

    # Accumulate stacked percentage leaks
    deduction_rate = freight_rate + tariff_rate + channel_markup_rate

    return {vn.DEDUCTION_RATE: deduction_rate}


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
        DeductionRate = MerchantFreightRate + TariffRate + ChannelMarkupRate

        Where:
        - "MerchantFreightRate" maps to vn.MERCHANT_FREIGHT_RATE
        - "TariffRate" maps to vn.TARIFF_RATE
        - "ChannelMarkupRate" maps to vn.CHANNEL_MARKUP_RATE
        - "DeductionRate" maps to vn.DEDUCTION_RATE
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
        self._output_names = [vn.DEDUCTION_RATE]

        # Establishing required variables
        self._required_variables = []

        # Migrated from standard list footprint to map defaults transparently to 0.0
        self._optional_variables = {
            vn.MERCHANT_FREIGHT_RATE: 0.0,
            vn.TARIFF_RATE: 0.0,
            vn.CHANNEL_MARKUP_RATE: 0.0
        }
