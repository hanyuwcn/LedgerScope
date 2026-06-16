from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_tariff(variables: dict) -> dict:
    """
    Calculates the import tariff cost per unit.

    Mathematical Formula:
        UnitTariff = UnitRetailPrice * TariffRate

    Args:
        variables (dict): Unified context containing all mandatory variables,
            resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated unit tariff directly to
            the central pipeline registry.
            Example: {"UNIT_TARIFF": 5.00}
    """
    unit_retail_price = variables[vn.UNIT_RETAIL_PRICE]
    tariff_rate = variables[vn.TARIFF_RATE]

    unit_tariff = unit_retail_price * tariff_rate

    return {vn.UNIT_TARIFF: unit_tariff}


class UnitTariffModel(Model):
    """
    Pipeline calculation block responsible for determining the import
    duty/tariff cost per unit sold.

    Description:
        This model isolates the tariff burden per unit by applying the
        import duty percentage against the base retail price. This ensures
        that international trade costs are accurately factored into the
        unit-level cost structure.

    Calculation Equation:
        UnitTariff = UnitRetailPrice * TariffRate

        Where:
        - "UnitRetailPrice" maps to vn.UNIT_RETAIL_PRICE (Required)
        - "TariffRate" maps to vn.TARIFF_RATE (Required)
        - "UnitTariff" maps to vn.UNIT_TARIFF
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitTariffModel with standard boundary checks.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_unit_tariff
        self._output_names = [vn.UNIT_TARIFF]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.UNIT_RETAIL_PRICE,
            vn.TARIFF_RATE,
        ]
