from src.config import variable_names
from src.core.base_model import Model


def calculate_price_architecture(optional_variables: dict, **kwargs) -> dict:
    """
    Decomposes the consumer retail price into its constituent cost, friction, and margin components.

    Architectural Roadmap:
        1. Normalization: Future iterations should ingest outputs from DeductionRateModel
           directly to eliminate redundant parameter passing.
        2. Bridge Logic: This model currently acts as a passive observer; future development
           should integrate this as a gating node for 'Min-Profitability' checks.
        3. Currency Scaling: All per-unit metrics are normalized to the ledger currency (RMB)
           via USD_TO_RMB scaling.

    Mathematical Formulas:
        - units = UnitsPerOrder * Orders
        - CogsPerUnit = COGS / units
        - ProfitPerUnit = Profit / units
        - ShippingPerUnit = UnitRetail * ShippingRate * USDToRMB
        - TariffPerUnit = UnitRetail * TariffRate * USDToRMB
        - RetailMarginPerUnit = UnitRetail * ChannelMarkupRate * USDToRMB

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Operational metrics including REVENUE, COGS, and unit-level friction rates.

    Returns:
        dict: A consolidated breakdown of per-unit pricing leakages and profit capture.
    """
    units = kwargs[variable_names.UNITS_PER_ORDER] * kwargs[variable_names.ORDERS]
    unit_retail_price = kwargs[variable_names.UNIT_RETAIL]
    cogs = kwargs[variable_names.COGS]
    profit = kwargs[variable_names.PROFIT]

    # Pull defaults from configuration registry
    shipping_rate = kwargs.get(variable_names.SHIPPING_RATE, optional_variables[variable_names.SHIPPING_RATE])
    tariff_rate = kwargs.get(variable_names.TARIFF_RATE, optional_variables[variable_names.TARIFF_RATE])
    markup_rate = kwargs.get(variable_names.CHANNEL_MARKUP_RATE, optional_variables[variable_names.CHANNEL_MARKUP_RATE])
    usd_to_rmb = kwargs.get(variable_names.USD_TO_RMB, optional_variables[variable_names.USD_TO_RMB])

    # Compute breakdown (Waterfall sequence)
    cogs_per_unit = cogs / units
    profit_per_unit = profit / units
    shipping_cost = unit_retail_price * shipping_rate * usd_to_rmb
    tariff_cost = unit_retail_price * tariff_rate * usd_to_rmb
    retail_margin = unit_retail_price * markup_rate * usd_to_rmb

    return {
        variable_names.COGS_PER_UNIT: cogs_per_unit,
        variable_names.PROFIT_PER_UNIT: profit_per_unit,
        variable_names.SHIPPING_COST_PER_UNIT: shipping_cost,
        variable_names.TARIFF_PER_UNIT: tariff_cost,
        variable_names.RETAIL_MARGIN_PER_UNIT: retail_margin,
    }


class PriceArchitectureModel(Model):
    """
    Pipeline block for granular unit-economic decomposition (The Pricing Waterfall).

    Description:
        This model performs the 'post-mortem' analysis on retail pricing. It systematically
        strips the retail price into its constituent financial components: manufacturing costs,
        logistical friction, import duties, distributor premiums, and final bottom-line profit.

    Calculation Equation:
        RetailPrice = COGS + Shipping + Tariff + RetailerMargin + NetProfit

        Where:
        - "CogsPerUnit" maps to variable_names.COGS_PER_UNIT
        - "ProfitPerUnit" maps to variable_names.PROFIT_PER_UNIT
        - "ShippingCostPerUnit" maps to variable_names.SHIPPING_COST_PER_UNIT
        - "TariffPerUnit" maps to variable_names.TARIFF_PER_UNIT
        - "RetailMarginPerUnit" maps to variable_names.RETAIL_MARGIN_PER_UNIT

    Architectural Roadmap (Future Stages):
        - Stage 2: Integration of sensitivity analysis to test margin compression.
        - Stage 3: Automated flagging of units where 'ProfitPerUnit' falls below threshold.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = calculate_price_architecture
        self._output_names = [
            variable_names.COGS_PER_UNIT,
            variable_names.PROFIT_PER_UNIT,
            variable_names.SHIPPING_COST_PER_UNIT,
            variable_names.TARIFF_PER_UNIT,
            variable_names.RETAIL_MARGIN_PER_UNIT,
        ]

        self._required_variables = [
            variable_names.UNITS_PER_ORDER,
            variable_names.ORDERS,
            variable_names.COGS,
            variable_names.UNIT_RETAIL,
            variable_names.PROFIT
        ]

        self._optional_variables = {
            variable_names.SHIPPING_RATE: 0.0,
            variable_names.TARIFF_RATE: 0.0,
            variable_names.CHANNEL_MARKUP_RATE: 0.0,
            variable_names.USD_TO_RMB: 1.0
        }
