import math

from src.config import variable_names as vn, settings
from src.core import Auditor


def check_deduction(variables: dict) -> None:
    """
    Validates that the deduction rates are within a logical range (0-1) and that
    the total retail price correctly reconciles with the FOB price and all
    associated USD deductions.

    Reconciliation Formula:
        1. DeductionRate = TariffRate + FreightRate + ChannelMarkupRate
        2. UnitRetailPrice(USD) = UnitFobPrice(USD) + UnitFreightExpense(USD) +
                                  UnitTariff(USD) + UnitRetailMargin(USD)

    Args:
        variables (dict): Unified context containing all rate and price components,
            pre-merged by the base Model orchestrator.

    Raises:
        ValueError: If deduction rates are out of bounds or if the pricing
            waterfall does not reconcile within the configured tolerance levels.
    """
    tariff_rate = variables[vn.TARIFF_RATE]
    freight_rate = variables[vn.FREIGHT_RATE]
    channel_markup_rate = variables[vn.CHANNEL_MARKUP_RATE]
    deduction_rate = tariff_rate + freight_rate + channel_markup_rate

    unit_fob_price = variables[vn.UNIT_FOB_PRICE]
    unit_freight_expense = variables[vn.UNIT_FREIGHT_EXPENSE]
    unit_tariff = variables[vn.UNIT_TARIFF]
    unit_retail_margin = variables[vn.UNIT_RETAIL_MARGIN]
    unit_retail_price = variables[vn.UNIT_RETAIL_PRICE]

    # Audit 1: Rate Range Validation (0 < DeductionRate < 1)
    if deduction_rate < 0:
        raise ValueError(f"deduction_rate({deduction_rate}) < 0")
    if deduction_rate > 1:
        raise ValueError(f"deduction_rate({deduction_rate}) > 1")

    # Audit 2: Price Waterfall Reconciliation (FOB + Deductions == Retail)
    if not math.isclose(unit_fob_price + unit_freight_expense + unit_tariff + unit_retail_margin,
                        unit_retail_price,
                        rel_tol=settings.AUDIT_REL_TOL,
                        abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(
            f"Reconciliation error: unit_fob_price({unit_fob_price}) "
            f"+ unit_freight_expense({unit_freight_expense}) "
            f"+ unit_tariff({unit_tariff}) "
            f"+ unit_retail_margin({unit_retail_margin}) "
            f"!= unit_retail_price({unit_retail_price})"
        )


class DeductionAuditor(Auditor):
    """
    Pipeline guardrail ensuring deduction rate logic and price waterfall accuracy.

    Description:
        This auditor validates two primary constraints:
        1. Rate Integrity: Ensures the cumulative impact of tariff, freight,
           and channel markup rates remains within a valid operational bounds (0-100%).
        2. Pricing Reconciliation: Ensures that the sum of the FOB value and all
           component costs (Freight, Tariff, Margin) equates to the defined Retail Price.

    Audit Logic:
        - Ensures: 0 < Sum(DeductionRates) < 1
        - Ensures: UnitRetailPrice == Sum(FOB, Freight, Tariff, Margin)
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_deduction

        self._required_variables = [
            vn.UNIT_FOB_PRICE,
            vn.UNIT_RETAIL_PRICE,
        ]

        self._optional_variables = {
            vn.TARIFF_RATE: 0.0,
            vn.UNIT_TARIFF: 0.0,
            vn.FREIGHT_RATE: 0.0,
            vn.UNIT_FREIGHT_EXPENSE: 0.0,
            vn.CHANNEL_MARKUP_RATE: 0.0,
            vn.UNIT_RETAIL_MARGIN: 0.0,
        }
