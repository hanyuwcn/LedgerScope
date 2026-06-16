from src.auditors import PriceArchitectureAuditor, DeductionAuditor, UnitGrossProfitAuditor, UnitOperatingIncomeAuditor

from src.models import (
    AdvertisingEfficiencyGoogleSearchModel, CostOfGoodsSoldModel,
    UnitFixedOverheadExpenseModel, BrandFreightExpenseModel, UnitMarketingExpenseModel,
    TotalSellingExpenseModel, TotalManagementExpenseModel, AdvertisingExpenseModel,
    UnitRetailMarginModel, UnitTariffModel,
    RevenueModel, TotalExpenseModel, DepreciationModel, CapitalExpenditureModel,
    NetIncomeModel, GrossProfitModel, RoiModel, FreeCashFlowModel, UnitFobModel,
    UnitGrossProfitModel, CacModel, CostPerLeadGoogleSearchModel,
    DeductionRateModel, OrderModel, MarketPriceModel, RoasModel, MonthlyExpenseModel, CurrencyExchangeModel,
    UnitOperatingIncomeModel, OperatingIncomeModel,
)

# The Global Model Menu
PIPELINE_REGISTRY = {
    # Models
    "advertising_efficiency_google_search": AdvertisingEfficiencyGoogleSearchModel,
    "cost_per_lead_google_search": CostPerLeadGoogleSearchModel,
    "deduction_rate": DeductionRateModel,
    "unit_fixed_overhead_expense": UnitFixedOverheadExpenseModel,
    "monthly_expense": MonthlyExpenseModel,
    "selling_expense": TotalSellingExpenseModel,
    "advertising_expense": AdvertisingExpenseModel,
    "management_expense": TotalManagementExpenseModel,
    "brand_freight_expense": BrandFreightExpenseModel,
    "currency_exchange": CurrencyExchangeModel,
    "order": OrderModel,
    "cogs": CostOfGoodsSoldModel,
    "revenue": RevenueModel,
    "unit_retail_margin": UnitRetailMarginModel,
    "unit_tariff": UnitTariffModel,
    "total_expense": TotalExpenseModel,
    "depreciation": DepreciationModel,
    "capital_expenditure": CapitalExpenditureModel,
    "unit_marketing_expense": UnitMarketingExpenseModel,
    "net_income": NetIncomeModel,
    "unit_operating_income": UnitOperatingIncomeModel,
    "operating_income": OperatingIncomeModel,
    "gross_profit": GrossProfitModel,
    "free_cash_flow": FreeCashFlowModel,
    "unit_gross_profit": UnitGrossProfitModel,
    "unit_fob": UnitFobModel,
    "roi": RoiModel,
    "cac": CacModel,
    "roas": RoasModel,
    "market_price": MarketPriceModel,

    # Auditors
    "price_architecture_auditor": PriceArchitectureAuditor,
    "deduction_auditor": DeductionAuditor,
    "unit_gross_profit_auditor": UnitGrossProfitAuditor,
    "unit_operating_income_auditor": UnitOperatingIncomeAuditor,
}
