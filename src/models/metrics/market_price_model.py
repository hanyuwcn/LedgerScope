from src.config import variable_names, settings
from src.core.base_model import Model


def calculate_market_price(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the implied equity market price (valuation cap) using an annualized PE multiple.

    This function annualizes the net inflows over a designated operational time window
    and multiplies the resulting annualized earnings base by a market-implied valuation
    multiple (Price-to-Earnings ratio).

    Mathematical Formula:
        MonthlyNetIncome = NetIncome / Months
        AnnualizedEarnings = MonthlyNetIncome * 12
        MarketPrice = AnnualizedEarnings * PeRatio
                    = (NetIncome * 12 * PeRatio) / Months

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing active runtime simulation overrides:

            Mandatory Keys:
                NET_INCOME (float): The absolute net operating income captured over the tracking window.

            Optional Keys:
                MONTHS (int/float, optional): The time-series window length of the income data. Defaults to 1.
                PE_RATIO (float, optional): Equity multiplier representing market premium benchmarks.

    Returns:
        dict: A single-element dictionary mapping the computed implied market capitalization valuation.
            Example: {"MarketPrice": 960000.0}
    """
    net_income = kwargs[variable_names.NET_INCOME]

    # Extract default fallback parameter thresholds out of the parent configuration registry map
    default_months = optional_variables[variable_names.MONTHS]
    default_pe_ratio = optional_variables[variable_names.PE_RATIO]

    # Dynamically extract values from active runtime args or fallback safely to baseline profiles
    months = kwargs.get(variable_names.MONTHS, default_months)
    pe_ratio = kwargs.get(variable_names.PE_RATIO, default_pe_ratio)

    # Calculate time-weighted annualized market equity value
    market_price = (net_income * 12.0 * pe_ratio) / months

    return {variable_names.MARKET_PRICE: market_price}


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
        - "NetIncome" maps to variable_names.NET_INCOME
        - "Months" maps to variable_names.MONTHS
        - "PeRatio" maps to variable_names.PE_RATIO
        - "MarketPrice" maps to variable_names.MARKET_PRICE
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
        self._output_names = [variable_names.MARKET_PRICE]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            variable_names.NET_INCOME,
        ]

        # Establish default baselines: assume monthly income baseline (1 month) and bind standard P/E ratio
        self._optional_variables = {
            variable_names.MONTHS: 1,
            variable_names.PE_RATIO: settings.DEFAULT_PE_RATIO
        }
