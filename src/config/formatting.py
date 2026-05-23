from src.utils.formatting import *
from .variable_names import *

VARIABLE_FORMATTING_MAP = {
    MONTHS: lambda v: fmt(v),

    ### Expenses
    EXPENSE: lambda v: fmt(v, s='¥'),
    EXPENSE_MONTHLY_FEE: lambda v: fmt(v, s='¥'),
    EXPENSE_MONTHLY_RENT: lambda v: fmt(v, s='¥'),
    EXPENSE_RENDER_FEE: lambda v: fmt(v, s='¥'),
    EXPENSE_TRAVEL_FEE: lambda v: fmt(v, s='¥'),

    ### Investment
    CAPITAL_EXPENDITURE: lambda v: fmt(v, s='¥'),
    DEPRECIATION: lambda v: fmt(v, s='¥'),

    ### Deals
    DEAL_ORDERS: lambda v: fmt(v, d=1),
    DEAL_ITEMS_PER_ORDER: lambda v: fmt(v, d=1),
    DEAL_SELLING_PRICE: lambda v: fmt(v, s='$'),
    DEAL_PURCHASING_PRICE: lambda v: fmt(v, s='¥'),

    ### Finance
    FINANCE_TAX_RATE: lambda v: fmt(v, d=2, p=True),
    FINANCE_USD_TO_RMB: lambda v: fmt(v, d=2),
    FINANCE_INTEREST_RATE: lambda v: fmt(v, d=2, p=True),

    ### Costs
    COST: lambda v: fmt(v, s='¥'),
    COST_ADVERTISING: lambda v: fmt(v, s='¥'),
    COST_SHIPPING: lambda v: fmt(v, s='¥'),
    COST_COGS: lambda v: fmt(v, s='¥'),
    COST_MANAGEMENT: lambda v: fmt(v, s='¥'),
    COST_CPA: lambda v: fmt(v, d=1, s='$'),
    COST_CONVERSION_RATE: lambda v: fmt(v, d=2, p=True),

    ### Revenue
    REVENUE: lambda v: fmt(v, s='¥'),
    REVENUE_GOODS_SOLD: lambda v: fmt(v, s='¥'),

    ### Metrics
    NET_INCOME: lambda v: fmt(v, s='¥'),
    PROFIT: lambda v: fmt(v, s='¥'),
    ROI: lambda v: fmt(v, d=2, p=True),
    FREE_CASH_FLOW: lambda v: fmt(v, s='¥')
}
