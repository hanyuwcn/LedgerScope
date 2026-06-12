"""
LedgerScope Model Registry.

Exposes all functional evaluation blocks as unified, first-class calculation 
nodes.
"""
# 1. Advertising
from .advertising.advertising_efficiency_google_search_model import AdvertisingEfficiencyGoogleSearchModel
from .advertising.cost_per_lead_google_search_model import CostPerLeadGoogleSearchModel

# 2. Cost
from .cost.shipping_cost_model import ShippingCostModel
from .cost.total_cost_model import TotalCostModel
from .cost.cost_of_goods_sold_model import CostOfGoodsSoldModel

# 3. Deal
from .deal.deduction_rate_model import DeductionRateModel
from .deal.order_model import OrderModel
from .deal.unit_fob_model import UnitFobModel
from .deal.unit_contribution_margin_model import UnitContributionMarginModel

# 4. Expense
from .expense.monthly_expense_model import MonthlyExpenseModel
from .expense.total_expense_model import TotalExpenseModel

# 5. Finance
from .finance.depreciation_model import DepreciationModel
from .finance.capital_expenditure_model import CapitalExpenditureModel

# 6. Revenue, Profit and Income
from .income.free_cash_flow_model import FreeCashFlowModel
from .income.net_income_model import NetIncomeModel
from .income.profit_model import ProfitModel
from .income.revenue_model import RevenueModel

# 7. Performance Metric Blocks
from .metrics.roi_model import RoiModel
from .metrics.roas_model import RoasModel
from .metrics.cac_model import CacModel
from .metrics.market_price_model import MarketPriceModel
from .metrics.price_architecture_model import PriceArchitectureModel

__all__ = [
    "AdvertisingEfficiencyGoogleSearchModel", "CostPerLeadGoogleSearchModel",
    "OrderModel", "DepreciationModel", "DeductionRateModel",
    "CapitalExpenditureModel", "CostOfGoodsSoldModel", "MonthlyExpenseModel",
    "TotalExpenseModel", "ShippingCostModel", "TotalCostModel", "UnitFobModel",
    "UnitContributionMarginModel", "RevenueModel", "NetIncomeModel",
    "ProfitModel", "FreeCashFlowModel", "RoiModel", "RoasModel",
    "CacModel", "MarketPriceModel", "PriceArchitectureModel",
]
