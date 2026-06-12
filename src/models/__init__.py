"""
LedgerScope Model Registry.

Exposes all functional evaluation blocks as unified, first-class calculation 
nodes.
"""
from .advertising.advertising_efficiency_google_search_model import AdvertisingEfficiencyGoogleSearchModel
from .advertising.cost_per_lead_google_search_model import CostPerLeadGoogleSearchModel
from .cost.cost_of_goods_sold_model import CostOfGoodsSoldModel
from .cost.shipping_cost_model import ShippingCostModel
from .cost.total_cost_model import TotalCostModel
from .deal.deduction_rate_model import DeductionRateModel
from .deal.order_model import OrderModel
from .deal.unit_contribution_margin_model import UnitContributionMarginModel
from .deal.unit_fob_model import UnitFobModel
from .expense.monthly_expense_model import MonthlyExpenseModel
from .expense.total_expense_model import TotalExpenseModel
from .finance.capital_expenditure_model import CapitalExpenditureModel
from .finance.depreciation_model import DepreciationModel
from .income.free_cash_flow_model import FreeCashFlowModel
from .income.net_income_model import NetIncomeModel
from .income.profit_model import ProfitModel
from .income.revenue_model import RevenueModel
from .metrics.cac_model import CacModel
from .metrics.market_price_model import MarketPriceModel
from .metrics.price_architecture_model import PriceArchitectureModel
from .metrics.roas_model import RoasModel
from .metrics.roi_model import RoiModel

__all__ = [
    # 1. Advertising
    "AdvertisingEfficiencyGoogleSearchModel",
    "CostPerLeadGoogleSearchModel",

    # 2. Cost
    "ShippingCostModel",
    "TotalCostModel",
    "CostOfGoodsSoldModel",

    # 3. Deal
    "DeductionRateModel",
    "OrderModel",
    "UnitFobModel",
    "UnitContributionMarginModel",

    # 4. Expense
    "MonthlyExpenseModel",
    "TotalExpenseModel",

    # 5. Finance
    "DepreciationModel",
    "CapitalExpenditureModel",

    # 6. Revenue, Profit and Income
    "FreeCashFlowModel",
    "NetIncomeModel",
    "ProfitModel",
    "RevenueModel",

    # 7. Performance Metric Blocks
    "RoiModel",
    "RoasModel",
    "CacModel",
    "MarketPriceModel",
    "PriceArchitectureModel",
]
