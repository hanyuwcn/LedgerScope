# src/ledgerscope/models/__init__.py

"""
LedgerScope Model Registry.

Exposes all functional evaluation blocks as unified, first-class calculation 
nodes to the pipeline engine execution layer.
"""

# 1. Marketing & Acquisition Node Layer
from .advertising_efficiency_model import AdvertisingEfficiencyModel
from .capital_expenditure_model import CapitalExpenditureModel
from .cost_model import TotalCostModel
from .cost_of_goods_sold_model import CostOfGoodsSoldModel
# 2. Asset & Operational Cost Aggregators
from .depreciation_model import DepreciationModel
from .expense_model import ExpenseModel
from .free_cash_flow_model import FreeCashFlowModel
from .net_income_model import NetIncomeModel
from .profit_model import ProfitModel
# 3. Income & Performance Metric Blocks
from .revenue_model import RevenueModel
from .roi_model import RoiModel

# Explicitly register public exposure hooks for clean pipeline importing
__all__ = [
    # Marketing
    "AdvertisingEfficiencyModel",

    # Aggregators
    "DepreciationModel",
    "CapitalExpenditureModel",
    "CostOfGoodsSoldModel",
    "ExpenseModel",
    "TotalCostModel",

    # Metrics / Ratios
    "RevenueModel",
    "NetIncomeModel",
    "ProfitModel",
    "RoiModel",
    "FreeCashFlowModel",
]
