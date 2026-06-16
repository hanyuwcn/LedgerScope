from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_unit_merchant_freight_expense(variables: dict) -> dict:
    """
    Calculates the consolidated shipping (freight) cost for unit-level logistics.

    Mathematical Formula:
        UnitMerchantFreightExpense = UnitRetailPrice * MerchantFreightRate

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the computed unit freight
            expense to the central pipeline registry.
            Example: {"UnitMerchantFreightExpense": 45.50}
    """
    unit_retail_price = variables[vn.UNIT_RETAIL_PRICE]
    unit_merchant_freight_rate = variables[vn.MERCHANT_FREIGHT_RATE]

    unit_merchant_freight_expense = unit_retail_price * unit_merchant_freight_rate

    return {vn.UNIT_MERCHANT_FREIGHT_EXPENSE: unit_merchant_freight_expense}


class UnitMerchantFreightExpenseModel(Model):
    """
    Pipeline calculation block responsible for assessing unit-level freight logistics.

    Description:
        This model acts as an essential expense-side node within the pipeline. It
        calculates the unit freight burden, enabling accurate assessment of margins
        by accounting for the variable logistics cost of moving a single unit
        through the fulfillment ecosystem.

    Calculation Equation:
        UnitMerchantFreightExpense = UnitRetailPrice * MerchantFreightRate

        Where:
        - "UnitRetailPrice" maps to vn.UNIT_RETAIL_PRICE
        - "MerchantFreightRate" maps to vn.MERCHANT_FREIGHT_RATE
        - "UnitMerchantFreightExpense" maps to vn.UNIT_MERCHANT_FREIGHT_EXPENSE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the UnitMerchantFreightExpenseModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional logic and mapping outputs to the central registry
        self._model_function = calculate_unit_merchant_freight_expense
        self._output_names = [vn.UNIT_MERCHANT_FREIGHT_EXPENSE]

        # Establishing dependencies for the pipeline layer
        self._required_variables = [
            vn.UNIT_RETAIL_PRICE,
        ]

        # Mapping defaults transparently to facilitate baseline logistics simulations
        self._optional_variables = {
            vn.MERCHANT_FREIGHT_RATE: 0.0,
        }
