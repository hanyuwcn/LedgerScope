"""
LedgerScope Model Registry.

Exposes all functional evaluation blocks as unified, first-class calculation 
nodes to the pipeline engine execution layer.

MAKE SURE THE ORDER OF THIS IMPORT DOES NOT CHANGE WHEN REFORMAT THE CODE.
IMPORTING PipelineComposer AT THE TOP MIGHT GENERATE CIRCULAR IMPORT ERROR
"""
# 1. Advertising
from .advertising.advertising_efficiency_model import AdvertisingEfficiencyModel
from .advertising.advertising_efficiency_google_search_model import AdvertisingEfficiencyGoogleSearchModel
from .advertising.cost_per_lead_google_search_model import CostPerLeadGoogleSearchModel

# 2. Aggregators
from .aggregators.depreciation_model import DepreciationModel
from .aggregators.expense_model import TotalExpenseModel
from .aggregators.capital_expenditure_model import CapitalExpenditureModel
from .aggregators.cost_model import TotalCostModel
from .aggregators.cost_of_goods_sold_model import CostOfGoodsSoldModel

# 3. Revenue, Profit and Income
from .income.free_cash_flow_model import FreeCashFlowModel
from .income.net_income_model import NetIncomeModel
from .income.profit_model import ProfitModel
from .income.revenue_model import RevenueModel

# 4. Performance Metric Blocks
from .metrics.roi_model import RoiModel
from .metrics.roas_model import ReturnOnAdvertisingSpendModel

# 5. Model Composer
from .composer.model_composer import PipelineComposer

# Explicitly register public exposure hooks for clean pipeline importing
__all__ = [
    # 1. Advertising / Funnel Analysis
    "AdvertisingEfficiencyModel",
    "AdvertisingEfficiencyGoogleSearchModel",
    "CostPerLeadGoogleSearchModel",

    # 2. Aggregators
    "DepreciationModel",
    "CapitalExpenditureModel",
    "CostOfGoodsSoldModel",
    "TotalExpenseModel",
    "TotalCostModel",

    # 3. Revenue, Profit and Income
    "RevenueModel",
    "NetIncomeModel",
    "ProfitModel",
    "FreeCashFlowModel",

    # 4. Performance Metrics / Ratios
    "RoiModel",
    "ReturnOnAdvertisingSpendModel",

    # 5. Model Composer
    "PipelineComposer",
]