from src.auditors import PriceArchitectureAuditor
from src.models import (
    AdvertisingEfficiencyGoogleSearchModel, CostOfGoodsSoldModel, TotalCostModel,
    RevenueModel, TotalExpenseModel, DepreciationModel, CapitalExpenditureModel,
    NetIncomeModel, ProfitModel, RoiModel, FreeCashFlowModel, UnitFobModel,
    UnitContributionMarginModel, CacModel, CostPerLeadGoogleSearchModel,
    DeductionRateModel, OrderModel, MarketPriceModel, RoasModel, PriceArchitectureModel, MonthlyExpenseModel
)

# The Global Model Menu
PIPELINE_REGISTRY = {
    # Models (The legacy list + any new ones)
    "advertising_efficiency_google_search": AdvertisingEfficiencyGoogleSearchModel,
    "cost_per_lead_google_search": CostPerLeadGoogleSearchModel,
    "deduction_rate": DeductionRateModel,
    "monthly_expense": MonthlyExpenseModel,
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
    "unit_fob": UnitFobModel,
    "roi": RoiModel,
    "cac": CacModel,
    "roas": RoasModel,
    "market_price": MarketPriceModel,
    "price_architecture": PriceArchitectureModel,

    # Auditors (The new additions)
    "price_architecture_auditor": PriceArchitectureAuditor,
}
