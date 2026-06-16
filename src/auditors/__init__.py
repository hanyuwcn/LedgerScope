"""
LedgerScope Auditor Registry.

Exposes all pipeline verification and integrity guardrails as first-class
nodes. These auditors perform post-calculation reconciliation to halt
pipeline execution if financial or logical invariants are violated.

DO NOT REORDER IMPORTS. MAINTAIN ALIGNMENT WITH CORRESPONDING MODELS.
"""

from .deduction_auditor import DeductionAuditor
from .price_architecture_auditor import PriceArchitectureAuditor
from .unit_gross_profit_auditor import UnitGrossProfitAuditor
from .unit_operating_income_auditor import UnitOperatingIncomeAuditor

# Explicitly register public exposure hooks for clean pipeline importing
__all__ = [
    "PriceArchitectureAuditor",
    "UnitGrossProfitAuditor",
    "UnitOperatingIncomeAuditor",
    "DeductionAuditor",
]
