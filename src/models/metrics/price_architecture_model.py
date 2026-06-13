from src.config import variable_names
from src.core.base_model import Model


def calculate_price_architecture(variables: dict) -> dict:
    """
    Decomposes the consumer retail price into its constituent cost,
    friction, and margin components.

    Mathematical Formulas:
        - units = UnitsPerOrder * Orders
        - CogsPerUnit = COGS / units
        - ProfitPerUnit = Profit / units
        - ShippingPerUnit = UnitRetail * ShippingRate * USDToRMB
        - TariffPerUnit = UnitRetail * TariffRate * USDToRMB
        - RetailMarginPerUnit = UnitRetail * ChannelMarkupRate * USDToRMB

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A consolidated breakdown of per-unit pricing leakages and profit capture.
    """
    units = variables[variable_names.UNITS_PER_ORDER] * variables[variable_names.ORDERS]
    unit_retail_price = variables[variable_names.UNIT_RETAIL]
    cogs = variables[variable_names.COGS]
    profit = variables[variable_names.PROFIT]

    shipping_rate = variables[variable_names.SHIPPING_RATE]
    tariff_rate = variables[variable_names.TARIFF_RATE]
    markup_rate = variables[variable_names.CHANNEL_MARKUP_RATE]
    usd_to_rmb = variables[variable_names.USD_TO_RMB]

    # Compute breakdown (Waterfall sequence)
    # Note: Ensure units > 0 in upstream validation
    cogs_per_unit = cogs / units if units != 0 else 0
    profit_per_unit = profit / units if units != 0 else 0

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
