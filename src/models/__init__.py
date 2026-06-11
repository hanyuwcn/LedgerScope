"""
LedgerScope Model Registry.

Exposes all functional evaluation blocks as unified, first-class calculation 
nodes.
"""
# 1. Advertising
from .advertising.advertising_efficiency_google_search_model import AdvertisingEfficiencyGoogleSearchModel
from .advertising.cost_per_lead_google_search_model import CostPerLeadGoogleSearchModel

# 2. Aggregators
from .aggregators.depreciation_model import DepreciationModel
from .aggregators.monthly_expense_model import MonthlyExpenseModel
from .aggregators.total_expense_model import TotalExpenseModel
from .aggregators.capital_expenditure_model import CapitalExpenditureModel
from .aggregators.total_cost_model import TotalCostModel
from .aggregators.cost_of_goods_sold_model import CostOfGoodsSoldModel
from .aggregators.deduction_rate_model import DeductionRateModel
from .aggregators.order_model import OrderModel
from .aggregators.unit_fob_model import UnitFobModel
from .aggregators.unit_contribution_margin_model import UnitContributionMarginModel

# 3. Revenue, Profit and Income
from .income.free_cash_flow_model import FreeCashFlowModel
from .income.net_income_model import NetIncomeModel
from .income.profit_model import ProfitModel
from .income.revenue_model import RevenueModel

# 4. Performance Metric Blocks
from .metrics.roi_model import RoiModel
from .metrics.roas_model import RoasModel
from .metrics.cac_model import CacModel
from .metrics.market_price_model import MarketPriceModel
from .metrics.price_architecture_model import PriceArchitectureModel

__all__ = [
    "AdvertisingEfficiencyGoogleSearchModel", "CostPerLeadGoogleSearchModel",
    "OrderModel", "DepreciationModel", "DeductionRateModel",
    "CapitalExpenditureModel", "CostOfGoodsSoldModel", "MonthlyExpenseModel",
    "TotalExpenseModel", "TotalCostModel", "UnitFobModel",
    "UnitContributionMarginModel", "RevenueModel", "NetIncomeModel",
    "ProfitModel", "FreeCashFlowModel", "RoiModel", "RoasModel",
    "CacModel", "MarketPriceModel", "PriceArchitectureModel",
]