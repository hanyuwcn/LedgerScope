import math

from src.config import variable_names as vn, settings
from src.core import Auditor


def check_price_architecture(variables: dict) -> None:
    """
    Validates the Price Waterfall for a single product context.

    Note: Cost and Profit are denominated in RMB.
          FOB, Retail, Shipping, and Tariff are denominated in USD.

    Mathematical Formulas:
        - UnitFob(RMB) = CostPerUnit + ProfitPerUnit
        - RetailPrice(USD) = UnitFob(USD) + Shipping + Tariff + RetailMargin

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Raises:
        ValueError: If the calculated components do not reconcile with
            the UnitFob or UnitRetail.
    """
    cost_per_unit = variables[vn.COST_PER_UNIT]
    profit_per_unit = variables[vn.PROFIT_PER_UNIT]
    unit_fob = variables[vn.UNIT_FOB]
    unit_retail_price = variables[vn.UNIT_RETAIL]
    shipping_cost_per_unit = variables[vn.SHIPPING_COST_PER_UNIT]
    tariff_per_unit = variables[vn.TARIFF_PER_UNIT]
    retail_margin_per_unit = variables[vn.RETAIL_MARGIN_PER_UNIT]
    usd_to_rmb = variables[vn.USD_TO_RMB]

    # Audit 1: Cost + Profit (RMB) == FOB (USD * Rate) (RMB)
    if not math.isclose(cost_per_unit + profit_per_unit, unit_fob * usd_to_rmb,
                        rel_tol=settings.AUDIT_REL_TOL, abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(f"Reconciliation error: cost_per_unit({cost_per_unit}) "
                         f"+ profit_per_unit({profit_per_unit}) "
                         f"!= unit_fob_in_rmb({unit_fob * usd_to_rmb})")

    # Audit 2: FOB + Deductions (USD) == Retail (USD)
    if not math.isclose(unit_fob + shipping_cost_per_unit + tariff_per_unit + retail_margin_per_unit,
                        unit_retail_price,
                        rel_tol=settings.AUDIT_REL_TOL, abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(f"Reconciliation error: unit_fob({unit_fob}) "
                         f"+ shipping_cost_per_unit({shipping_cost_per_unit}) "
                         f"+ tariff_per_unit({tariff_per_unit}) "
                         f"+ retail_margin_per_unit({retail_margin_per_unit}) "
                         f"!= unit_retail_price({unit_retail_price})")


class PriceArchitectureAuditor(Auditor):
    """
    Pipeline guardrail to verify the Pricing Waterfall decomposition.

    Description:
        This auditor reconciles the unit-economic breakdown (RMB) against
        international trade values (USD).

        Note: Cost and Profit are in RMB; FOB, Retail, Shipping, and
        Tariff are in USD.

    Reconciliation Logic:
        1. Base Value: (Cost_per_unit + Profit_per_unit) == (Unit_FOB * USD_TO_RMB)
        2. Full Waterfall: Unit_FOB + Shipping + Tariff + Margin == Unit_Retail
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_price_architecture

        self._required_variables = [
            vn.COST_PER_UNIT,
            vn.PROFIT_PER_UNIT,
            vn.UNIT_FOB,
            vn.UNIT_RETAIL,
        ]

        self._optional_variables = {
            vn.SHIPPING_COST_PER_UNIT: 0.0,
            vn.TARIFF_PER_UNIT: 0.0,
            vn.RETAIL_MARGIN_PER_UNIT: 0.0,
            vn.USD_TO_RMB: 1.0,
        }
