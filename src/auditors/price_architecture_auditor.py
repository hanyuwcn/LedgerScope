import math

from src.config import variable_names as vn, settings
from src.core import Auditor


def check_price_architecture(variables: dict) -> None:
    """
    Validates that the sum of all individual unit-level cost and margin
    components reconciles with the total Unit Retail Price.

    Reconciliation Formula:
        UnitRetailPrice = (UnitEXWPrice + UnitMarketingExpense +
                          UnitFixedOverheadExpense + UnitOperatingIncome +
                          UnitFreightExpense + UnitTariffExpense +
                          UnitRetailMargin)

    Args:
        variables (dict): Unified context containing all price components
            normalized to RMB, pre-merged by the base Model orchestrator.

    Raises:
        ValueError: If the sum of components deviates from the Retail Price
            beyond the configured tolerance levels.
    """
    unit_retail_price = variables[vn.UNIT_RETAIL_PRICE_IN_RMB]
    unit_exw_price = variables[vn.UNIT_EXW_PRICE]
    unit_marketing_expense = variables[vn.UNIT_MARKETING_EXPENSE]
    unit_fixed_overhead_expense = variables[vn.UNIT_FIXED_OVERHEAD_EXPENSE]
    unit_operating_income = variables[vn.UNIT_OPERATING_INCOME]
    unit_freight_expense = variables[vn.UNIT_FREIGHT_EXPENSE_IN_RMB]
    unit_tariff_expense = variables[vn.UNIT_TARIFF_IN_RMB]
    unit_retail_margin = variables[vn.UNIT_RETAIL_MARGIN_IN_RMB]

    if not math.isclose(unit_exw_price
                        + unit_marketing_expense
                        + unit_fixed_overhead_expense
                        + unit_operating_income
                        + unit_freight_expense
                        + unit_tariff_expense
                        + unit_retail_margin,
                        unit_retail_price,
                        rel_tol=settings.AUDIT_REL_TOL,
                        abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(
            f"Reconciliation error: unit_exw_price({unit_exw_price}) "
            f"+ unit_marketing_expense({unit_marketing_expense}) "
            f"+ unit_fixed_overhead_expense({unit_fixed_overhead_expense}) "
            f"+ unit_operating_income({unit_operating_income}) "
            f"+ unit_freight_expense({unit_freight_expense}) "
            f"+ unit_tariff_expense({unit_tariff_expense}) "
            f"+ unit_retail_margin({unit_retail_margin}) "
            f"!= unit_retail_price({unit_retail_price})"
        )


class PriceArchitectureAuditor(Auditor):
    """
    Pipeline guardrail ensuring price waterfall integrity.

    Description:
        This auditor verifies that all constituent costs and margins in the
        unit-level price waterfall aggregate to the final retail price.
        It acts as a circuit breaker for the calculation pipeline.
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_price_architecture

        self._required_variables = [
            vn.UNIT_RETAIL_PRICE_IN_RMB,
            vn.UNIT_EXW_PRICE,
            vn.UNIT_OPERATING_INCOME,
        ]

        self._optional_variables = {
            vn.UNIT_FIXED_OVERHEAD_EXPENSE: 0.0,
            vn.UNIT_MARKETING_EXPENSE: 0.0,
            vn.UNIT_FREIGHT_EXPENSE_IN_RMB: 0.0,
            vn.UNIT_TARIFF_IN_RMB: 0.0,
            vn.UNIT_RETAIL_MARGIN_IN_RMB: 0.0
        }
