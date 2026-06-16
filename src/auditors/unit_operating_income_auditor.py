import math

from src.config import variable_names as vn, settings
from src.core import Auditor


def check_operating_income(variables: dict) -> None:
    """
    Validates that the Unit Operating Income reconciles with the product
    margin after accounting for marketing and fixed overheads.

    Note: Unit Brand Freight Expense is forcibly set to 0.0 as this is a
          non-brand-borne expense in the current business model.

    Reconciliation Formula:
        UnitOperatingIncome = (UnitFobPriceInRMB - UnitExwPrice -
                               UnitMarketingExpense - UnitBrandFreightExpense -
                               UnitFixedOverheadExpense)

    Args:
        variables (dict): Unified context containing price components.

    Raises:
        ValueError: If the calculated result deviates from the provided
            operating income beyond configured tolerance levels.
    """
    unit_operating_income = variables[vn.UNIT_OPERATING_INCOME]
    unit_fob_price = variables[vn.UNIT_FOB_PRICE_IN_RMB]
    unit_exw_price = variables[vn.UNIT_EXW_PRICE]
    unit_marketing_expense = variables[vn.UNIT_MARKETING_EXPENSE]
    unit_fixed_overhead_expense = variables[vn.UNIT_FIXED_OVERHEAD_EXPENSE]

    # Brand-side business rule: Freight is not borne by the brand
    unit_brand_freight_expense = 0.0

    if not math.isclose(unit_fob_price
                        - unit_exw_price
                        - unit_marketing_expense
                        - unit_brand_freight_expense
                        - unit_fixed_overhead_expense,
                        unit_operating_income,
                        rel_tol=settings.AUDIT_REL_TOL,
                        abs_tol=settings.AUDIT_ABS_TOL):
        raise ValueError(
            f"Reconciliation error: unit_fob_price_in_rmb({unit_fob_price}) "
            f"- unit_exw_price({unit_exw_price}) "
            f"- unit_marketing_expense({unit_marketing_expense}) "
            f"- unit_brand_freight_expense({unit_brand_freight_expense}) "
            f"- unit_fixed_overhead_expense({unit_fixed_overhead_expense}) "
            f"!= unit_operating_income({unit_operating_income})"
        )


class UnitOperatingIncomeAuditor(Auditor):
    """
    Pipeline guardrail ensuring unit-level operating profitability integrity.

    Description:
        This auditor validates that Operating Income is correctly derived from
        FOB (RMB) and EXW pricing while enforcing business rules regarding
        non-brand expenses (e.g., freight).

    Audit Logic:
        - Ensures: OperatingIncome == (FOB_RMB - EXW - Marketing - BrandFreight(0) - FixedOverhead)
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_operating_income

        self._required_variables = [
            vn.UNIT_OPERATING_INCOME,
            vn.UNIT_FOB_PRICE_IN_RMB,
            vn.UNIT_EXW_PRICE,
        ]

        self._optional_variables = {
            vn.UNIT_MARKETING_EXPENSE: 0.0,
            vn.UNIT_FIXED_OVERHEAD_EXPENSE: 0.0,
            vn.BRAND_FREIGHT_EXPENSE: 0.0,
        }
