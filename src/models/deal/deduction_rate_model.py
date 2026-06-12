from src.config import variable_names
from src.core.base_model import Model


def calculate_deduction_rate(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the aggregate gross margin deduction rate leakage coefficient.

    This function rolls up the disparate, non-production friction elements that map the
    spread between consumer retail pricing structures and contractual port delivery
    valuations (FOB). It aggregates logistical transport components, international trade
    tariffs, and localized ecosystem distributor margins.

    Mathematical Formula:
        DeductionRate = ShippingRate + TariffRate + ChannelMarkupRate

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing active runtime simulation overrides:

            Optional Keys:
                SHIPPING_RATE (float, optional): Logistical transport friction percentage.
                TARIFF_RATE (float, optional): Macro-economic cross-border import duty percentage.
                CHANNEL_MARKUP_RATE (float, optional): Distributor/retailer ecosystem premium percentage.

    Returns:
        dict: A single-element dictionary mapping the calculated combined leak coefficient
            to its master registry key signature.
            Example: {"DeductionRate": 0.43}
    """
    # Extract default fallback baseline rates from the centralized parameter registry map
    default_shipping_rate = optional_variables[variable_names.SHIPPING_RATE]
    default_tariff_rate = optional_variables[variable_names.TARIFF_RATE]
    default_channel_markup_rate = optional_variables[variable_names.CHANNEL_MARKUP_RATE]

    # Dynamically pull simulation sweeps from active runtime kwargs, falling back cleanly to registry defaults
    shipping_rate = kwargs.get(variable_names.SHIPPING_RATE, default_shipping_rate)
    tariff_rate = kwargs.get(variable_names.TARIFF_RATE, default_tariff_rate)
    channel_markup_rate = kwargs.get(variable_names.CHANNEL_MARKUP_RATE, default_channel_markup_rate)

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
