from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_merchant_attributes_in_rmb(variables: dict) -> dict:
    """
    Converts a suite of merchant-side unit metrics from USD to RMB.

    Mathematical Formula:
        AttributeInRMB = AttributeInUSD * USDToRMBExchangeRate

    Args:
        variables (dict): Unified context containing the exchange rate and
            relevant attributes in USD.

    Returns:
        dict: A dictionary containing the converted values for retail price,
            freight expense, tariff, retail margin, and FOB price in RMB.
    """
    currency_exchange_rate = variables[vn.USD_TO_RMB]

    return {vn.UNIT_RETAIL_PRICE_IN_RMB: variables[vn.UNIT_RETAIL_PRICE] * currency_exchange_rate,
            vn.UNIT_FREIGHT_EXPENSE_IN_RMB: variables[vn.UNIT_FREIGHT_EXPENSE] * currency_exchange_rate,
            vn.UNIT_TARIFF_IN_RMB: variables[vn.UNIT_TARIFF] * currency_exchange_rate,
            vn.UNIT_RETAIL_MARGIN_IN_RMB: variables[vn.UNIT_RETAIL_MARGIN] * currency_exchange_rate,
            vn.UNIT_FOB_PRICE_IN_RMB: variables[vn.UNIT_FOB_PRICE] * currency_exchange_rate,
            }


class CurrencyExchangeModel(Model):
    """
    Pipeline calculation block responsible for normalizing merchant unit economics
    into a single reporting currency (RMB).

    Description:
        This model facilitates multi-currency financial reporting by applying a
        singular exchange rate across all primary unit-level metrics. It ensures
        that downstream profit and cost analysis can be performed in RMB
        regardless of the initial currency of the input metrics.

    Calculation Equation:
        ConvertedValue = OriginalValue * USDToRMB

        Where:
        - "USDToRMB" maps to vn.USD_TO_RMB (Required)
        - Inputs are normalized by multiplying by the exchange rate.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the CurrencyExchangeModel with standardized currency conversion boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_merchant_attributes_in_rmb
        self._output_names = [
            vn.UNIT_RETAIL_PRICE_IN_RMB,
            vn.UNIT_FREIGHT_EXPENSE_IN_RMB,
            vn.UNIT_TARIFF_IN_RMB,
            vn.UNIT_RETAIL_MARGIN_IN_RMB,
            vn.UNIT_FOB_PRICE_IN_RMB,
        ]

        # Explicit tracking validation boundaries
        self._required_variables = [
            vn.USD_TO_RMB,
        ]

        self._optional_variables = {
            vn.UNIT_RETAIL_PRICE: 0.0,
            vn.UNIT_FREIGHT_EXPENSE: 0.0,
            vn.UNIT_TARIFF: 0.0,
            vn.UNIT_RETAIL_MARGIN: 0.0,
            vn.UNIT_FOB_PRICE: 0.0,
        }
