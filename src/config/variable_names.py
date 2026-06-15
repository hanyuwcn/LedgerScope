## Variable Names

SYSTEM_RUN_ID = "simulation_run_id"
MODEL_DEFAULT_OUTPUT_NAME = "Output"

### Below are the common Variable names
MONTHS = "Months"

### Below are the Variable names, which MUST matches the correspondant argument names in the aggregation functions
### Expenses
EXPENSE = "Expense"

#### Management Expense
RENT_EXPENSE = "RentExpense"
RENDER_EXPENSE = "RenderExpense"
TRAVEL_EXPENSE = "TravelExpense"
MONTHLY_MANAGEMENT_EXPENSE = "MonthlyManagementExpense"
MANAGEMENT_EXPENSE = "ManagementExpense"
UNIT_FIXED_OVERHEAD_EXPENSE = "UnitFixedOverheadExpense"

#### Selling Expense
MARKETING_EXPENSE = "MarketingExpense"
UNIT_MARKETING_EXPENSE = "UnitMarketingExpense"
ADVERTISING_EXPENSE = "AdvertisingExpense"
FREIGHT_EXPENSE = "FreightExpense"

### Ads
CONVERSION_RATE_GOOGLE_SEARCH = "GoogleSearchConversionRate"
CPC_GOOGLE_SEARCH = "GoogleSearchCostPerClick"
ALLOCATION_GOOGLE_SEARCH = "AllocationGoogleSearch"
CPL_GOOGLE_SEARCH = "GoogleSearchCostPerLeads"
LEADS = "Leads"

### Brand
ORDERS = "Orders"
CLOSE_RATE = "CloseRate"
UNITS_PER_ORDER = "UnitsPerOrder"
UNITS_SOLD = "UnitsSold"
UNIT_EXW_PRICE = "UnitExWorksPrice"
UNIT_FOB_PRICE = "UnitFreeOnBoardPrice"

### Merchant
UNIT_RETAIL_PRICE = "UnitRetailPrice"
UNIT_RETAIL_PRICE_IN_RMB = "UnitRetailPrice(RMB)"
DEDUCTION_RATE = "DeductionRate"
CHANNEL_MARKUP_RATE = "ChannelMarkupRate"
FREIGHT_RATE = "FreightRate"
UNIT_FREIGHT_EXPENSE = "UnitFreightExpense"
UNIT_FREIGHT_EXPENSE_IN_RMB = "UnitFreightExpense(RMB)"
UNIT_TARIFF = "UnitTariff"
UNIT_TARIFF_IN_RMB = "UnitTariff(RMB)"
UNIT_RETAIL_MARGIN = "UnitRetailerMargin"
UNIT_RETAIL_MARGIN_IN_RMB = "UnitRetailerMargin(RMB)"

### Finance
TAX_RATE = "TaxRate"
TARIFF_RATE = "TariffRate"
USD_TO_RMB = "USDToRMB"
INTEREST_RATE = "InterestRate"

### Costs
COGS = "Cogs"
COST = "Cost"

### Income
REVENUE = "Revenue"
# REVENUE_GOODS_SOLD = "GoodsSold"
NET_INCOME = "NetIncome"
PROFIT = "Profit"
UNIT_GROSS_PROFIT = "UnitGrossProfit"
FREE_CASH_FLOW = "FreeCashFlow"

### Investment
CAPITAL_EXPENDITURE = "CapitalExpenditure"
DEPRECIATION = "Depreciation"
SETUP_INVESTMENT = "SetupInvestment"
PE_RATIO = "PriceToEarningsRatio"
MARKET_PRICE = "MarketPrice"

### Price Architecture
# COST_PER_UNIT = "CostPerUnit"
# SHIPPING_COST_PER_UNIT = "ShippingCostPerUnit"
# UNIT_CONTRIBUTION_MARGIN = "UnitContributionMargin"


### Metrics
ROI = "ROI"
ROAS = "ReturnOnAdvertisingSpend"
CAC = "CustomerAcquisitionCost"

## Break even analysis
BREAK_EVEN_VARIABLE_NAME = "BreakEvenVariable"
BREAK_EVEN_EXPECTED_VARIABLE_VALUE = "BreakEvenExpectedVariableValue"
BREAK_EVEN_EXPECTED_RESULT = "BreakEvenExpectedResult"
BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE = "ThresholdVariableValue"
BREAK_EVEN_POINT_THRESHOLD_RESULT = "ThresholdResult"
BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE = "SafetyMarginPercentage"
BREAK_EVEN_FEASIBILITY_STATUS = "FeasibilityStatus"

## Comparative statics
COMPARATIVE_STATICS_VARIABLE_NAME = "ComparativeStaticsVariable"
COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE = "ComparativeStaticsExpectedVariableValue"
COMPARATIVE_STATICS_EXPECTED_RESULT = "ComparativeStaticsExpectedResult"
COMPARATIVE_STATICS_MIN_VARIABLE_VALUE = "ComparativeStaticsMinVariableValue"
COMPARATIVE_STATICS_MIN_RESULT = "ComparativeStaticsMinResult"
COMPARATIVE_STATICS_MAX_VARIABLE_VALUE = "ComparativeStaticsMaxVariableValue"
COMPARATIVE_STATICS_MAX_RESULT = "ComparativeStaticsMaxResult"
COMPARATIVE_STATICS_ELASTICITY = "ComparativeStaticsElasticity"
