from src.models import (
    AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel,
    RevenueModel, TotalExpenseModel, DepreciationModel, CapitalExpenditureModel,
    NetIncomeModel, ProfitModel, RoiModel, FreeCashFlowModel
)

# The Global Model Menu
MODEL_REGISTRY = {
    "advertising_efficiency": AdvertisingEfficiencyModel,
    "cogs": CostOfGoodsSoldModel,
    "total_cost": TotalCostModel,
    "revenue": RevenueModel,
    "total_expense": TotalExpenseModel,
    "depreciation": DepreciationModel,
    "capital_expenditure": CapitalExpenditureModel,
    "net_income": NetIncomeModel,
    "profit": ProfitModel,
    "roi": RoiModel,
    "free_cash_flow": FreeCashFlowModel
}
