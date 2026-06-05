"""
LedgerScope Primitive Declarations.

Aggregates and exposes the unified financial and transactional variables 
across costs, logistical deals, operational overhead, and currency matrices.
"""

from .advertising import (
    AdvertisingBudget,
    GoogleSearchConversionRate,
    GoogleSearchCostPerClick,
    GoogleSearchAllocationPercentage,
)
from .costs import Cost, SetupCost, AdvertisingCost, CostPerAcquisition, \
    ConversionRate  # CPA & ConversionRate are pending deprecation
from .deals import Orders, CloseRate, ItemsPerOrder, SellingPrice, PurchasingPrice
from .expenses import Rent, TravelFee, RenderFee, Expense
from .finance import InterestRate, TaxRate, USDToRMB

__all__ = [
    # Costs
    "Cost",
    "SetupCost",
    "AdvertisingCost",
    "CostPerAcquisition",  # TODO: Deprecate once new ads funnel model fully deployed
    "ConversionRate",  # TODO: Deprecate once new ads funnel model fully deployed

    # Deals
    "Orders",
    "CloseRate",
    "ItemsPerOrder",
    "SellingPrice",
    "PurchasingPrice",

    # Expenses
    "Rent",
    "TravelFee",
    "RenderFee",
    "Expense",

    # Finance
    "InterestRate",
    "TaxRate",
    "USDToRMB",

    # Performance Marketing & Advertising Funnel
    "AdvertisingBudget",
    "GoogleSearchConversionRate",
    "GoogleSearchCostPerClick",
    "GoogleSearchAllocationPercentage",
]
