from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_net_income(variables: dict) -> dict:
    """
    Calculates the Net Income After Tax.

    Mathematical Formula:
        NetIncome = OperatingIncome * (1 - TaxRate)

    Args:
        variables (dict): Unified context containing the operating income
            and the applicable tax rate.

    Returns:
        dict: A dictionary mapping the net income metric to the
            primary pipeline registry key.
    """
    operating_income = variables[vn.OPERATING_INCOME]
    tax_rate = variables[vn.TAX_RATE]

    # Calculate net income by applying the tax rate to operating income
    calculated_net_income = operating_income * (1.0 - tax_rate)

    return {vn.NET_INCOME: calculated_net_income}


class NetIncomeModel(Model):
    """
    Pipeline calculation block responsible for evaluating net profitability
    after statutory tax obligations.

    Description:
        Net Income represents the final measure of a business unit's financial
        health. This model applies the corporate tax rate to the provided
        Operating Income to derive the after-tax profitability.

    Calculation Equation:
        NetIncome = OperatingIncome * (1.0 - TaxRate)

        Where:
        - "OperatingIncome" maps to vn.OPERATING_INCOME (Required)
        - "TaxRate" maps to vn.TAX_RATE (Optional, default 0.0)
        - "NetIncome" maps to vn.NET_INCOME
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the NetIncomeModel with standardized tax boundary configurations.

        Args:
            input_variables (dict, optional): The active runtime configuration
                context dictionary.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_net_income
        self._output_names = [vn.NET_INCOME]

        # Operating income is the mandatory prerequisite for net income calculation
        self._required_variables = [
            vn.OPERATING_INCOME,
        ]

        # Tax rate is optional; defaults to 0.0 (no tax) if not specified
        self._optional_variables = {
            vn.TAX_RATE: 0.0
        }
