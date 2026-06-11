"""
LedgerScope Auditor Registry.

Exposes all pipeline verification and integrity guardrails as first-class
nodes. These auditors perform post-calculation reconciliation to halt
pipeline execution if financial or logical invariants are violated.

DO NOT REORDER IMPORTS. MAINTAIN ALIGNMENT WITH CORRESPONDING MODELS.
"""

# 1. Performance and Pricing Auditors
from .price_architecture_auditor import PriceArchitectureAuditor

# 2. Add future auditors here (e.g., revenue_auditor, margin_auditor)
# from .income.revenue_auditor import RevenueAuditor

# Explicitly register public exposure hooks for clean pipeline importing
__all__ = [
    # 1. Performance and Pricing
    "PriceArchitectureAuditor",

    # 2. Income/Revenue
    # "RevenueAuditor",
]
