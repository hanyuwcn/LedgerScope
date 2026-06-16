from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_operating_income(variables: dict) -> dict:
    """
    Calculates the operating income generated per individual unit sold.

    Mathematical Formula:
        UnitOperatingIncome = OperatingIncome / UnitsSold

    Args:
        variables (dict): Unified context containing the total operating income
            and the total units sold.

    Returns:
        dict: A dictionary mapping the calculated unit operating income
            to the primary pipeline registry.
            Example: {"UNIT_OPERATING_INCOME": 50.0}
    """
    operating_income = variables[vn.OPERATING_INCOME]
    units_sold = variables[vn.UNITS_SOLD]

    # Handle division by zero for scenarios with no sales volume
    if units_sold == 0:
        return {vn.UNIT_OPERATING_INCOME: 0.0}

    calculated_unit_operating_income = operating_income / units_sold
    return {vn.UNIT_OPERATING_INCOME: calculated_unit_operating_income}


class UnitOperatingIncomeModel(Model):
    """
    Pipeline calculation block responsible for determining operational
    profitability on a per-unit basis.

    Description:
        This model derives the Unit Operating Income by normalizing the total
        period operating income against the total units sold. It allows
        stakeholders to observe the effective operational profit yield of
        every item sold, serving as a foundational metric for unit economics.

    Calculation Equation:
        UnitOperatingIncome = OperatingIncome / UnitsSold

        Where:
        - "OperatingIncome" maps to vn.OPERATING_INCOME (Required)
        - "UnitsSold" maps to vn.UNITS_SOLD (Required)
        - "UnitOperatingIncome" maps to vn.UNIT_OPERATING_INCOME
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitOperatingIncomeModel with mandatory accounting requirements.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_unit_operating_income
        self._output_names = [vn.UNIT_OPERATING_INCOME]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.OPERATING_INCOME,
            vn.UNITS_SOLD,
        ]

        self._optional_variables = {}
