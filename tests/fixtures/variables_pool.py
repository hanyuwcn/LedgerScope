# from src.config import variable_names
# from src.variables import (
#     Expense,
#     Rent,
#     TravelFee,
#     RenderFee,
#     Cost,
#     SetupCost,
#     AdvertisingCost,
#     CostPerAcquisition,
#     ConversionRate,
#     Orders,
#     CloseRate,
#     InterestRate,
#     TaxRate,
#     USDToRMB
# )
#
#
# def get_test_variable_portfolio() -> dict:
#     """
#     Centralized factory providing a standard, isolated portfolio of all
#     LedgerScope domain variables with default test boundaries.
#
#     Returns:
#         dict: A map of string-token registry keys to initialized Variable domain instances.
#     """
#     return {
#         # Expenses
#         variable_names.EXPENSE: Expense(expected_value=1000, min_value=500, max_value=2000),
#         variable_names.EXPENSE_MONTHLY_RENT: Rent(min_value=1000, max_value=3000),
#         variable_names.EXPENSE_TRAVEL_FEE: TravelFee(max_value=1500),
#         variable_names.EXPENSE_RENDER_FEE: RenderFee(min_value=1000, max_value=2000),
#
#         # Costs
#         variable_names.COST: Cost(),
#         variable_names.COST_SETUP: SetupCost(min_value=6000, max_value=15000),
#         variable_names.COST_ADVERTISING: AdvertisingCost(min_value=10000, max_value=30000),
#         variable_names.COST_CPA: CostPerAcquisition(min_value=12, max_value=36),
#         variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.04, max_value=0.2),
#
#         # Deals
#         variable_names.REVENUE: 0,
#         variable_names.DEAL_ORDERS: Orders(min_value=20, max_value=30),
#         variable_names.CLOSE_RATE: CloseRate(min_value=0.08, max_value=0.18),
#         variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=1, max_value=5),
#         variable_names.DEAL_SELLING_PRICE: SellingPrice(min_value=3000, max_value=6000),
#         variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=1000, max_value=2000),
#
#         # Finance
#         variable_names.FINANCE_INTEREST_RATE: InterestRate(expected_value=0.05),
#         variable_names.FINANCE_TAX_RATE: TaxRate(expected_value=0.2),
#         variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5),
#     }
