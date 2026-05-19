# src/ledgerscope/variables/__init__.py

"""
LedgerScope Primitive Declarations.

Aggregates and exposes the unified financial and transactional variables 
across costs, logistical deals, operational overhead, and currency matrices.
"""

from .costs import Cost, AdvertisingCost, CostPerAcquisition, ConversionRate
from .deals import Orders, ItemsPerOrder, SellingPrice, PurchasingPrice
from .expenses import Rent, TravelFee, RenderFee, Expense
from .finance import InterestRate, TaxRate, USDToRMB

__all__ = [
    # Costs
    "Cost",
    "AdvertisingCost",
    "CostPerAcquisition",
    "ConversionRate",

    # Deals
    "Orders",
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
]
