from src.utils.formatting import *
from .variable_names import *

VARIABLE_FORMATTING_MAP = {
    MONTHS: lambda v: fmt(v),

    ### Advertising
    CONVERSION_RATE_GOOGLE_SEARCH: lambda v: fmt(v, d=2, p=True),
    CPC_GOOGLE_SEARCH: lambda v: fmt(v, d=1, s='$'),
    ALLOCATION_GOOGLE_SEARCH: lambda v: fmt(v, d=0, p=True),
    CPL_GOOGLE_SEARCH: lambda v: fmt(v, d=1, s='$'),
    LEADS: lambda v: fmt(v, d=1),

    ### Expenses
    EXPENSE: lambda v: fmt(v, s='¥'),
    MONTHLY_EXPENSE: lambda v: fmt(v, s='¥'),
    RENT_EXPENSE: lambda v: fmt(v, s='¥'),
    RENDER_EXPENSE: lambda v: fmt(v, s='¥'),
    TRAVEL_EXPENSE: lambda v: fmt(v, s='¥'),

    ### Investment
    CAPITAL_EXPENDITURE: lambda v: fmt(v, s='¥'),
    DEPRECIATION: lambda v: fmt(v, s='¥'),

    ### Deals
    ORDERS: lambda v: fmt(v, d=1),
    CLOSE_RATE: lambda v: fmt(v, d=2, p=True),
    UNITS_PER_ORDER: lambda v: fmt(v, d=1),
    UNIT_FOB: lambda v: fmt(v, s='$'),
    UNIT_EXW: lambda v: fmt(v, s='¥'),

    ### Finance
    TAX_RATE: lambda v: fmt(v, d=2, p=True),
    USD_TO_RMB: lambda v: fmt(v, d=2),
    INTEREST_RATE: lambda v: fmt(v, d=2, p=True),

    ### Costs
    COST: lambda v: fmt(v, s='¥'),
    ADVERTISING_COST: lambda v: fmt(v, s='¥'),
    SHIPPING_COST: lambda v: fmt(v, s='¥'),
    COGS: lambda v: fmt(v, s='¥'),
    MANAGEMENT_COST: lambda v: fmt(v, s='¥'),

    ### Revenue
    REVENUE: lambda v: fmt(v, s='¥'),
    REVENUE_GOODS_SOLD: lambda v: fmt(v, s='¥'),
    NET_INCOME: lambda v: fmt(v, s='¥'),
    PROFIT: lambda v: fmt(v, s='¥'),
    FREE_CASH_FLOW: lambda v: fmt(v, s='¥'),

    ### Price Architecture
    COST_PER_UNIT: lambda v: fmt(v, d=1, s='¥'),
    SHIPPING_COST_PER_UNIT: lambda v: fmt(v, s='¥'),
    TARIFF_PER_UNIT: lambda v: fmt(v, s='¥'),
    RETAIL_MARGIN_PER_UNIT: lambda v: fmt(v, s='¥'),
    PROFIT_PER_UNIT: lambda v: fmt(v, s='¥'),

    ### Metrics
    ROI: lambda v: fmt(v, d=2, p=True),
    ROAS: lambda v: fmt(v, d=1, p=True),
    CAC: lambda v: fmt(v, d=1, s='¥'),
    UNIT_CONTRIBUTION_MARGIN: lambda v: fmt(v, s='¥'),
    MARKET_PRICE: lambda v: fmt(v, s='¥'),
}
