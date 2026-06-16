import math

from src.config import variable_names as vn, settings
from src.core import Auditor


def check_unit_gross_profit(variables: dict) -> None:
    """
    Validates that the Unit Gross Profit reconciles correctly with the 
    difference between the Unit FOB Price (RMB) and the Unit EXW Price.

    Reconciliation Formula:
        UnitGrossProfit = UnitFobPriceInRMB - UnitExwPrice

    Args:
        variables (dict): Unified context containing the price components,
            pre-merged by the base Model orchestrator.

    Raises:
        ValueError: If the calculated gross profit deviates from the
            expected value beyond configured tolerance levels.
    """
    unit_fob_price = variables[vn.UNIT_FOB_PRICE_IN_RMB]
    unit_exw_price = variables[vn.UNIT_EXW_PRICE]
    unit_gross_profit = variables[vn.UNIT_GROSS_PROFIT]

    if not math.isclose(unit_fob_price - unit_exw_price,
                        unit_gross_profit,
                        rel_tol=settings.AUDIT_REL_TOL,
                        abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(
            f"Reconciliation error: unit_fob_price_in_rmb({unit_fob_price}) "
            f"- unit_exw_price({unit_exw_price}) "
            f"!= unit_gross_profit({unit_gross_profit})"
        )


class UnitGrossProfitAuditor(Auditor):
    """
    Pipeline guardrail ensuring unit-level gross profit integrity using RMB metrics.

    Description:
        This auditor verifies the margin calculation at the FOB stage.
        It ensures that the value added (Gross Profit) is mathematically
        consistent with the factory-gate cost and the final FOB price (in RMB)
        before the product enters the downstream retail waterfall.

    Audit Logic:
        - Ensures: UnitGrossProfit == (UnitFobPriceInRMB - UnitExwPrice)
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_unit_gross_profit

        self._required_variables = [
            vn.UNIT_FOB_PRICE_IN_RMB,
            vn.UNIT_EXW_PRICE,
            vn.UNIT_GROSS_PROFIT,
        ]
