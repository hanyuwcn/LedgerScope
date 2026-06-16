from src.utils.formatting import *
from .variable_names import *

VARIABLE_FORMATTING_MAP = {
    ### Common
    MONTHS: lambda v: fmt(v),

    ### Expenses
    EXPENSE: lambda v: fmt(v, s='¥'),

    #### Management Expense
    RENT_EXPENSE: lambda v: fmt(v, s='¥'),
    RENDER_EXPENSE: lambda v: fmt(v, s='¥'),
    TRAVEL_EXPENSE: lambda v: fmt(v, s='¥'),
    MONTHLY_MANAGEMENT_EXPENSE: lambda v: fmt(v, s='¥'),
    MANAGEMENT_EXPENSE: lambda v: fmt(v, s='¥'),
    UNIT_FIXED_OVERHEAD_EXPENSE: lambda v: fmt(v, s='¥'),

    #### Selling Expense
    MARKETING_EXPENSE: lambda v: fmt(v, s='¥'),
    UNIT_MARKETING_EXPENSE: lambda v: fmt(v, d=1, s='$'),
    ADVERTISING_EXPENSE: lambda v: fmt(v, s='¥'),
    BRAND_FREIGHT_EXPENSE: lambda v: fmt(v, d=1, s='$'),
    SELLING_EXPENSE: lambda v: fmt(v, d=1, s='$'),

    ### Advertising
    CONVERSION_RATE_GOOGLE_SEARCH: lambda v: fmt(v, d=2, p=True),
    CPC_GOOGLE_SEARCH: lambda v: fmt(v, d=1, s='$'),
    ALLOCATION_GOOGLE_SEARCH: lambda v: fmt(v, d=0, p=True),
    CPL_GOOGLE_SEARCH: lambda v: fmt(v, d=1, s='$'),
    LEADS: lambda v: fmt(v, d=1),

    ### Brand
    ORDERS: lambda v: fmt(v, d=1),
    CLOSE_RATE: lambda v: fmt(v, d=2, p=True),
    UNITS_PER_ORDER: lambda v: fmt(v, d=1),
    UNITS_SOLD: lambda v: fmt(v, d=1),
    UNIT_EXW_PRICE: lambda v: fmt(v, s='¥'),
    COGS: lambda v: fmt(v, s='¥'),
    COST: lambda v: fmt(v, s='¥'),

    ### Merchant
    UNIT_RETAIL_PRICE: lambda v: fmt(v, s='$'),
    UNIT_RETAIL_PRICE_IN_RMB: lambda v: fmt(v, s='¥'),
    DEDUCTION_RATE: lambda v: fmt(v, d=1, p=True),
    CHANNEL_MARKUP_RATE: lambda v: fmt(v, d=1, p=True),
    MERCHANT_FREIGHT_RATE: lambda v: fmt(v, d=1, p=True),
    UNIT_MERCHANT_FREIGHT_EXPENSE: lambda v: fmt(v, d=1, s='$'),
    UNIT_MERCHANT_FREIGHT_EXPENSE_IN_RMB: lambda v: fmt(v, d=1, s='¥'),
    UNIT_TARIFF: lambda v: fmt(v, s='$'),
    UNIT_TARIFF_IN_RMB: lambda v: fmt(v, s='¥'),
    UNIT_RETAIL_MARGIN: lambda v: fmt(v, s='$'),
    UNIT_RETAIL_MARGIN_IN_RMB: lambda v: fmt(v, s='¥'),
    UNIT_FOB_PRICE: lambda v: fmt(v, s='$'),
    UNIT_FOB_PRICE_IN_RMB: lambda v: fmt(v, s='¥'),

    ### Finance
    TAX_RATE: lambda v: fmt(v, d=2, p=True),
    TARIFF_RATE: lambda v: fmt(v, d=1, p=True),
    USD_TO_RMB: lambda v: fmt(v, d=2),
    INTEREST_RATE: lambda v: fmt(v, d=2, p=True),

    ### Income
    REVENUE: lambda v: fmt(v, s='¥'),
    GROSS_PROFIT: lambda v: fmt(v, s='¥'),
    UNIT_GROSS_PROFIT: lambda v: fmt(v, s='¥'),
    OPERATING_INCOME: lambda v: fmt(v, s='¥'),
    UNIT_OPERATING_INCOME: lambda v: fmt(v, s='¥'),
    NET_INCOME: lambda v: fmt(v, s='¥'),
    FREE_CASH_FLOW: lambda v: fmt(v, s='¥'),

    ### Investment
    CAPITAL_EXPENDITURE: lambda v: fmt(v, s='¥'),
    DEPRECIATION: lambda v: fmt(v, s='¥'),
    SETUP_INVESTMENT: lambda v: fmt(v, s='¥'),
    PE_RATIO: lambda v: fmt(v, d=1),
    MARKET_PRICE: lambda v: fmt(v, s='¥'),

    ### Price Architecture
    # COST_PER_UNIT: lambda v: fmt(v, d=1, s='¥'),
    # SHIPPING_COST_PER_UNIT: lambda v: fmt(v, s='¥'),

    ### Metrics
    ROI: lambda v: fmt(v, d=2, p=True),
    ROAS: lambda v: fmt(v, d=1, p=True),
    CAC: lambda v: fmt(v, d=1, s='¥'),
    # UNIT_CONTRIBUTION_MARGIN: lambda v: fmt(v, s='¥'),

}
