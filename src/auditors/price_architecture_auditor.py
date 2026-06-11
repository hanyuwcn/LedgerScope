import math

from src.config import variable_names, settings
from src.core import Auditor


def check_price_architecture(optional_variables: dict, **kwargs):
    """
    Validates the Price Waterfall for a single product context.

    Mathematical Formulas:
        - UnitFob = CogsPerUnit + ProfitPerUnit
        - RetailPrice = UnitFob + ShippingCostPerUnit + TariffPerUnit + RetailMarginPerUnit

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Operational unit-level economic metrics.

    Raises:
        ValueError: If the calculated components do not reconcile with the UnitFob or UnitRetail.
    """
    cogs_per_unit = kwargs[variable_names.COGS_PER_UNIT]
    profit_per_unit = kwargs[variable_names.PROFIT_PER_UNIT]
    unit_fob = kwargs[variable_names.UNIT_FOB]
    unit_retail_price = kwargs[variable_names.UNIT_RETAIL]

    # Pull defaults
    shipping_cost_per_unit = kwargs.get(variable_names.SHIPPING_COST_PER_UNIT,
                                        optional_variables[variable_names.SHIPPING_COST_PER_UNIT])
    tariff_per_unit = kwargs.get(variable_names.TARIFF_PER_UNIT,
                                 optional_variables[variable_names.TARIFF_PER_UNIT])
    retail_margin_per_unit = kwargs.get(variable_names.RETAIL_MARGIN_PER_UNIT,
                                        optional_variables[variable_names.RETAIL_MARGIN_PER_UNIT])

    # Audit 1: COGS + Profit == FOB
    if not math.isclose(cogs_per_unit + profit_per_unit, unit_fob,
                        rel_tol=settings.AUDIT_REL_TOL, abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(f"Reconciliation error: cog_per_unit({cogs_per_unit}) "
                         f"+ profit_per_unit({profit_per_unit}) "
                         f"!= unit_fob({unit_fob})")

    # Audit 2: FOB + Deductions == Retail
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
        This auditor functions as a critical integrity gate in the pipeline. It
        reconciles the unit-economic breakdown against the retail price anchor.
        If the internal financial components fail to sum to the expected retail
        value within the defined tolerances, this auditor halts pipeline
        execution to prevent the propagation of erroneous financial data.

    Constraint:
        This auditor is strictly scoped to process a single product context per
        execution. It does not perform batch aggregations.

    Reconciliation Logic:
        1. Base Value: COGS_per_unit + Profit_per_unit == Unit_FOB
        2. Full Waterfall: Unit_FOB + Shipping + Tariff + Margin == Unit_Retail

    Architectural Roadmap (Future Stages):
        - Stage 2: Integration of batch-level product ID checks.
        - Stage 3: Automated alert dispatching to the LedgerScope console on
          reconciliation failure.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_price_architecture

        self._required_variables = [
            variable_names.COGS_PER_UNIT,
            variable_names.PROFIT_PER_UNIT,
            variable_names.UNIT_FOB,
            variable_names.UNIT_RETAIL,
        ]

        self._optional_variables = {
            variable_names.SHIPPING_COST_PER_UNIT: 0.0,
            variable_names.TARIFF_PER_UNIT: 0.0,
            variable_names.RETAIL_MARGIN_PER_UNIT: 0.0,
        }
