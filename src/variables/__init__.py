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
from .costs import (
    Cost,
    SetupCost,
    AdvertisingCost,
)
from .deals import (
    Orders,
    CloseRate,
    UnitExw,
    UnitRetail,
    ChannelMarkupRate,
    ShippingRate,
    DeductionRate,
    UnitFob,
    UnitsPerOrder,
)
from .expenses import (
    Expense,
    MonthlyExpense,
    RentExpense,
    TravelExpense,
    RenderExpense,
)
from .finance import (
    InterestRate,
    TaxRate,
    TariffRate,
    USDToRMB,
    PriceToEarningsRatio,
)

__all__ = [
    # Performance Marketing & Advertising Funnel
    "AdvertisingBudget",
    "GoogleSearchConversionRate",
    "GoogleSearchCostPerClick",
    "GoogleSearchAllocationPercentage",

    # Costs
    "Cost",
    "SetupCost",
    "AdvertisingCost",

    # Deal Architecture (Margin Matrix & Volume Primitives)
    "Orders",
    "CloseRate",
    "UnitExw",
    "UnitRetail",
    "ChannelMarkupRate",
    "ShippingRate",
    "DeductionRate",
    "UnitFob",
    "UnitsPerOrder",

    # Operational Expenses
    "Expense",
    "MonthlyExpense",
    "RentExpense",
    "TravelExpense",
    "RenderExpense",

    # Macro Finance Metrics & Valuation Multipliers
    "InterestRate",
    "TaxRate",
    "TariffRate",
    "USDToRMB",
    "PriceToEarningsRatio",
]
