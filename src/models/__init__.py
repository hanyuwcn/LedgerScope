"""
LedgerScope Model Registry.

Exposes all functional evaluation blocks as unified, first-class calculation 
nodes.
"""
from .advertising.advertising_efficiency_google_search_model import AdvertisingEfficiencyGoogleSearchModel
from .advertising.cost_per_lead_google_search_model import CostPerLeadGoogleSearchModel
from .brand.cost_of_goods_sold_model import CostOfGoodsSoldModel
from .brand.order_model import OrderModel
from .brand.units_sold_model import UnitsSoldModel
from .expense.management.monthly_management_expense_model import MonthlyExpenseModel
from .expense.management.total_management_expense_model import TotalManagementExpenseModel
from .expense.management.unit_fixed_overhead_expense_model import UnitFixedOverheadExpenseModel
from .expense.selling.advertising_expense_model import AdvertisingExpenseModel
from .expense.selling.freight_expense_model import BrandFreightExpenseModel
from .expense.selling.total_selling_expense_model import TotalSellingExpenseModel
from .expense.selling.unit_marketing_expense_model import UnitMarketingExpenseModel
from .expense.total_expense_model import TotalExpenseModel
from .income.free_cash_flow_model import FreeCashFlowModel
from .income.gross_profit_model import GrossProfitModel
from .income.net_income_model import NetIncomeModel
from .income.operating_income_model import OperatingIncomeModel
from .income.revenue_model import RevenueModel
from .income.unit_gross_profit_model import UnitGrossProfitModel
from .income.unit_operating_income_model import UnitOperatingIncomeModel
from .investment.capital_expenditure_model import CapitalExpenditureModel
from .investment.depreciation_model import DepreciationModel
from .investment.market_price_model import MarketPriceModel
from .merchant.currency_exchange_model import CurrencyExchangeModel
from .merchant.deduction_rate_model import DeductionRateModel
from .merchant.unit_fob_price_model import UnitFobModel
from .merchant.unit_freight_expense_model import UnitMerchantFreightExpenseModel
from .merchant.unit_retail_margin_model import UnitRetailMarginModel
from .merchant.unit_tariff_model import UnitTariffModel
from .metrics.cac_model import CacModel
from .metrics.roas_model import RoasModel
from .metrics.roi_model import RoiModel

__all__ = [
    # 1. Expense
    "MonthlyExpenseModel",
    "TotalManagementExpenseModel",
    "UnitFixedOverheadExpenseModel",
    "BrandFreightExpenseModel",
    "UnitMarketingExpenseModel",
    "TotalExpenseModel",
    "AdvertisingExpenseModel",
    "TotalSellingExpenseModel",

    # 2. Advertising
    "AdvertisingEfficiencyGoogleSearchModel",
    "CostPerLeadGoogleSearchModel",

    # 3. Brand
    "OrderModel",
    "CostOfGoodsSoldModel",
    "UnitsSoldModel",

    # 4. Merchant
    "UnitMerchantFreightExpenseModel",
    "DeductionRateModel",
    "UnitFobModel",
    "UnitRetailMarginModel",
    "UnitTariffModel",
    "CurrencyExchangeModel",

    # 5. Revenue, Profit and Income
    "FreeCashFlowModel",
    "NetIncomeModel",
    "OperatingIncomeModel",
    "UnitOperatingIncomeModel",
    "GrossProfitModel",
    "UnitGrossProfitModel",
    "RevenueModel",

    # 6. Investment
    "DepreciationModel",
    "CapitalExpenditureModel",

    # 7. Performance Metric Blocks
    "RoiModel",
    "RoasModel",
    "CacModel",
    "MarketPriceModel",
]
