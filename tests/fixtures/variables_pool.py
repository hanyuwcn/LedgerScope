from src.config import variable_names

from src.variables import GoogleSearchConversionRate, GoogleSearchCostPerClick, \
    CloseRate, UnitsPerOrder, UnitExwPrice, RentExpense, RenderExpense, TravelExpense, MarketingExpense, \
    InterestRate, TaxRate, TariffRate, USDToRMB, \
    PriceToEarningsRatio, SetupInvestment, UnitRetailPrice, RetailMarginRate, MerchantFreightRate, \
    GoogleSearchAllocationPercentage


def get_panoramic_variable_portfolio() -> dict:
    """
    Centralized factory providing a standard, isolated portfolio of all
    LedgerScope domain variables with default test boundaries.

    Returns:
        dict: A map of string-token registry keys to initialized Variable domain instances.
    """
    return {
        variable_names.MARKETING_EXPENSE: MarketingExpense(3000, 4000, 5000),
        # variable_names.ADVERTISING_EXPENSE: AdvertisingBudget(2000, 3000, 5000),
        variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(min=0.04, max=0.06),
        variable_names.CPC_GOOGLE_SEARCH: GoogleSearchCostPerClick(min=1.80, exp=2.50, max=3.50),
        variable_names.ALLOCATION_GOOGLE_SEARCH: GoogleSearchAllocationPercentage(min=0.50, max=0.70),

        # variable_names.ORDERS: Orders(),
        variable_names.CLOSE_RATE: CloseRate(min=0.08, exp=0.12, max=0.18),
        variable_names.UNITS_PER_ORDER: UnitsPerOrder(min=1, max=5),
        # units_sold = UnitsSold(),
        variable_names.UNIT_EXW_PRICE: UnitExwPrice(min=2000, exp=3000, max=5000),

        # variable_names.UNIT_FOB_PRICE: UnitFobPrice(min=4000, exp=5000, max=6000),

        # variable_names.MONTHS: Months(exp=1),

        # expense = Expense(),
        variable_names.RENT_EXPENSE: RentExpense(min=1000, max=3000),
        variable_names.RENDER_EXPENSE: RenderExpense(min=1000, max=2000),
        variable_names.TRAVEL_EXPENSE: TravelExpense(max=1500),
        # monthly_management_expense = MonthlyManagementExpense(),

        # unit_marketing_expense = UnitMarketingExpense(),
        # advertising_expense = AdvertisingExpense(),
        # brand_freight_expense = BrandFreightExpense(),

        variable_names.INTEREST_RATE: InterestRate(exp=0.05),
        variable_names.TAX_RATE: TaxRate(exp=0.20),
        variable_names.TARIFF_RATE: TariffRate(min=0.15, exp=0.25, max=0.35),
        variable_names.USD_TO_RMB: USDToRMB(min=6.0, exp=6.8, max=7.5),

        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0),
        variable_names.SETUP_INVESTMENT: SetupInvestment(min=10000, exp=20000, max=30000),

        variable_names.UNIT_RETAIL_PRICE: UnitRetailPrice(min=8000, exp=10000, max=12000),
        # deduction_rate = DeductionRate(),
        variable_names.CHANNEL_MARKUP_RATE: RetailMarginRate(min=0.10, exp=0.15, max=0.20),
        variable_names.MERCHANT_FREIGHT_RATE: MerchantFreightRate(min=0.02, exp=0.05, max=0.08),
        # variable_names.UNIT_MERCHANT_FREIGHT_EXPENSE: UnitMerchantFreightExpense(),
        # unit_tariff = UnitTariff(),
        # unit_retail_margin = UnitRetailMargin(),
    }
