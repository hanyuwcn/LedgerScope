from src.config import variable_names as vn, settings
from src.core.base_model import Model


def calculate_market_price(variables: dict) -> dict:
    """
    Calculates the implied equity market price (valuation cap) using an annualized PE multiple.

    Mathematical Formula:
        MarketPrice = (NetIncome * 12 * PeRatio) / Months

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A single-element dictionary mapping the computed implied
            market capitalization valuation.
            Example: {"MARKET_PRICE": 960000.0}
    """
    net_income = variables[vn.NET_INCOME]
    months = variables[vn.MONTHS]
    pe_ratio = variables[vn.PE_RATIO]

    # Calculate time-weighted annualized market equity value
    market_price = (net_income * 12.0 * pe_ratio) / months

    return {vn.MARKET_PRICE: market_price}


class MarketPriceModel(Model):
    """
    Pipeline calculation block responsible for translating net profitability runs
    into macroeconomic enterprise market valuations.

    Description:
        This model functions as an equity valuation layer inside the income processing tier.
        By normalizing operational time-series windows and applying historical or simulated
        Price-to-Earnings (P/E) multipliers, it bridges baseline accounting profits directly
        to strategic investor exit valuations.

    Calculation Equation:
        MarketPrice = (NetIncome * 12 * PeRatio) / Months

        Where:
        - "NetIncome" maps to vn.NET_INCOME
        - "Months" maps to vn.MONTHS
        - "PeRatio" maps to vn.PE_RATIO
        - "MarketPrice" maps to vn.MARKET_PRICE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the MarketPriceModel with explicit validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_market_price
        self._output_names = [vn.MARKET_PRICE]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.NET_INCOME,
        ]

        # Establish default baselines: assume monthly income baseline (1 month) and bind standard P/E ratio
        self._optional_variables = {
            vn.MONTHS: 1,
            vn.PE_RATIO: settings.DEFAULT_PE_RATIO
        }
