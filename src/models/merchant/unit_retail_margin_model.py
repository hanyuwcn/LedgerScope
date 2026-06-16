from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_retail_margin(variables: dict) -> dict:
    """
    Calculates the retail margin per unit based on the retail price and markup rate.

    Mathematical Formula:
        UnitRetailMargin = UnitRetailPrice * ChannelMarkupRate

    Args:
        variables (dict): Unified context containing all mandatory variables,
            resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated unit retail margin directly to
            the central pipeline registry.
            Example: {"UNIT_RETAIL_MARGIN": 12.50}
    """
    unit_retail_price = variables[vn.UNIT_RETAIL_PRICE]
    channel_markup_rate = variables[vn.CHANNEL_MARKUP_RATE]

    unit_retail_margin = unit_retail_price * channel_markup_rate

    return {vn.UNIT_RETAIL_MARGIN: unit_retail_margin}


class UnitRetailMarginModel(Model):
    """
    Pipeline calculation block responsible for determining the margin contribution
    per unit attributed to the retail channel.

    Description:
        This model quantifies the dollar value retained by the retail partner
        per unit sold, calculated by applying the channel markup rate against
        the final retail price. It is a critical component for understanding
        total channel economics.

    Calculation Equation:
        UnitRetailMargin = UnitRetailPrice * ChannelMarkupRate

        Where:
        - "UnitRetailPrice" maps to vn.UNIT_RETAIL_PRICE (Required)
        - "ChannelMarkupRate" maps to vn.CHANNEL_MARKUP_RATE (Required)
        - "UnitRetailMargin" maps to vn.UNIT_RETAIL_MARGIN
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitRetailMarginModel with standard boundary checks.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_unit_retail_margin
        self._output_names = [vn.UNIT_RETAIL_MARGIN]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.UNIT_RETAIL_PRICE,
            vn.CHANNEL_MARKUP_RATE,
        ]
