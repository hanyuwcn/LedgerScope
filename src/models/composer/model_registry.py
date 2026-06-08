from src.models import (
    AdvertisingEfficiencyGoogleSearchModel, CostOfGoodsSoldModel, TotalCostModel,
    RevenueModel, TotalExpenseModel, DepreciationModel, CapitalExpenditureModel,
    NetIncomeModel, ProfitModel, RoiModel, FreeCashFlowModel,
    UnitContributionMarginModel, CacModel, CostPerLeadGoogleSearchModel, DeductionRateModel, OrderModel,
    MarketPriceModel, RoasModel
)

# The Global Model Menu
MODEL_REGISTRY = {
    "advertising_efficiency_google_search": AdvertisingEfficiencyGoogleSearchModel,
    "cost_per_lead_google_search": CostPerLeadGoogleSearchModel,
    "deduction_rate": DeductionRateModel,
    "monthly_expense": TotalExpenseModel,
    "order": OrderModel,
    "cogs": CostOfGoodsSoldModel,
    "total_cost": TotalCostModel,
    "revenue": RevenueModel,
    "total_expense": TotalExpenseModel,
    "depreciation": DepreciationModel,
    "capital_expenditure": CapitalExpenditureModel,
    "net_income": NetIncomeModel,
    "profit": ProfitModel,
    "free_cash_flow": FreeCashFlowModel,
    "unit_contribution_margin": UnitContributionMarginModel,
    "roi": RoiModel,
    "cac": CacModel,
    "roas": RoasModel,
    "market_price": MarketPriceModel
}
