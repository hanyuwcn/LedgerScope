from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_price_architecture(variables: dict) -> dict:
    """
    Decomposes the consumer retail price into its constituent cost,
    friction, and margin components.

    Mathematical Formulas:
        - units = UnitsPerOrder * Orders
        - CostPerUnit = TotalCost / units
        - ProfitPerUnit = Profit / units
        - ShippingPerUnit = UnitRetail * ShippingRate
        - TariffPerUnit = UnitRetail * TariffRate
        - RetailMarginPerUnit = UnitRetail * ChannelMarkupRate

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A consolidated breakdown of per-unit pricing leakages and profit capture.
    """
    units = variables[vn.UNITS_PER_ORDER] * variables[vn.ORDERS]
    unit_retail_price = variables[vn.UNIT_RETAIL]
    total_cost = variables[vn.COST]
    profit = variables[vn.PROFIT]

    shipping_rate = variables[vn.SHIPPING_RATE]
    tariff_rate = variables[vn.TARIFF_RATE]
    markup_rate = variables[vn.CHANNEL_MARKUP_RATE]

    # Compute breakdown (Waterfall sequence)
    # Note: Ensure units > 0 in upstream validation
    cost_per_unit = total_cost / units if units != 0 else 0
    profit_per_unit = profit / units if units != 0 else 0

    unit_shipping_cost = unit_retail_price * shipping_rate
    unit_tariff_cost = unit_retail_price * tariff_rate
    unit_retail_margin = unit_retail_price * markup_rate

    return {
        vn.COST_PER_UNIT: cost_per_unit,
        vn.PROFIT_PER_UNIT: profit_per_unit,
        vn.SHIPPING_COST_PER_UNIT: unit_shipping_cost,
        vn.TARIFF_PER_UNIT: unit_tariff_cost,
        vn.RETAIL_MARGIN_PER_UNIT: unit_retail_margin,
    }


class PriceArchitectureModel(Model):
    """
    Pipeline block for granular unit-economic decomposition (The Pricing Waterfall).

    Description:
        This model performs the 'post-mortem' analysis on retail pricing. It systematically
        strips the retail price into its constituent financial components: total operational
        costs, logistical friction, import duties, distributor premiums, and final
        bottom-line profit.

    Calculation Equation:
        RetailPrice = CostPerUnit + Shipping + Tariff + RetailerMargin + NetProfit

        Where:
        - "CostPerUnit" maps to vn.COST_PER_UNIT
        - "ProfitPerUnit" maps to vn.PROFIT_PER_UNIT
        - "ShippingCostPerUnit" maps to vn.SHIPPING_COST_PER_UNIT
        - "TariffPerUnit" maps to vn.TARIFF_PER_UNIT
        - "RetailMarginPerUnit" maps to vn.RETAIL_MARGIN_PER_UNIT

    Architectural Roadmap (Future Stages):
        - Stage 2: Integration of sensitivity analysis to test margin compression.
        - Stage 3: Automated flagging of units where 'ProfitPerUnit' falls below threshold.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = calculate_price_architecture
        self._output_names = [
            vn.COST_PER_UNIT,
            vn.PROFIT_PER_UNIT,
            vn.SHIPPING_COST_PER_UNIT,
            vn.TARIFF_PER_UNIT,
            vn.RETAIL_MARGIN_PER_UNIT,
        ]

        self._required_variables = [
            vn.UNITS_PER_ORDER,
            vn.COST,
            vn.ORDERS,
            vn.UNIT_RETAIL,
            vn.PROFIT
        ]

        self._optional_variables = {
            vn.SHIPPING_RATE: 0.0,
            vn.TARIFF_RATE: 0.0,
            vn.CHANNEL_MARKUP_RATE: 0.0
        }
