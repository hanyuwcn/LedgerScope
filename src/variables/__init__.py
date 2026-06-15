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
from .brand import (
    Orders,
    CloseRate,
    UnitsPerOrder,
    UnitsSold,
    UnitExwPrice,
    UnitFobPrice,
)
from .common import Months
from .expenses import (
    Expense,
    RentExpense,
    RenderExpense,
    TravelExpense,
    MonthlyManagementExpense,
    MarketingExpense,
    UnitMarketingExpense,
    AdvertisingExpense,
    FreightExpense,
)
from .finance import (
    InterestRate,
    TaxRate,
    TariffRate,
    USDToRMB,
)
from .investment import (
    PriceToEarningsRatio,
    SetupInvestment,
)
from .merchant import (
    UnitRetailPrice,
    DeductionRate,
    RetailMarginRate,
    FreightRate,
    UnitFreightExpense,
    UnitTariff,
    UnitRetailMargin,
)

__all__ = [
    # Common
    "Months",

    # Advertising
    "AdvertisingBudget",
    "GoogleSearchConversionRate",
    "GoogleSearchCostPerClick",
    "GoogleSearchAllocationPercentage",

    # Brand
    "Orders",
    "CloseRate",
    "UnitsPerOrder",
    "UnitsSold",
    "UnitExwPrice",
    "UnitFobPrice",

    # Merchant
    "UnitRetailPrice",
    "DeductionRate",
    "RetailMarginRate",
    "FreightRate",
    "UnitFreightExpense",
    "UnitTariff",
    "UnitRetailMargin",

    # Expenses
    "Expense",
    "RentExpense",
    "RenderExpense",
    "TravelExpense",
    "MonthlyManagementExpense",
    "MarketingExpense",
    "UnitMarketingExpense",
    "AdvertisingExpense",
    "FreightExpense",

    # Finance
    "InterestRate",
    "TaxRate",
    "TariffRate",
    "USDToRMB",

    # Investment
    "PriceToEarningsRatio",
    "SetupInvestment",
]
