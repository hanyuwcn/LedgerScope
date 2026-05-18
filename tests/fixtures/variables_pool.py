from src.config import COST_ADVERTISING, COST_CONVERSION_RATE, COST_CPA, FINANCE_USD_TO_RMB, FINANCE_TAX_RATE, \
    FINANCE_INTEREST_RATE, DEAL_ORDERS, DEAL_ITEMS_PER_ORDER, DEAL_SELLING_PRICE, REVENUE, DEAL_PURCHASING_PRICE, COST, \
    EXPENSE, EXPENSE_TRAVEL_FEE, EXPENSE_RENDER_FEE, EXPENSE_MONTHLY_RENT
from src.variables import (Expense, Rent, TravelFee, RenderFee,
                           Cost, AdvertisingCost, CostPerAcquisition, ConversionRate,
                           Orders, ItemsPerOrder, SellingPrice, PurchasingPrice,
                           InterestRate, TaxRate, USDToRMB)


def get_test_variable_portfolio() -> dict:
    """
    Centralized factory providing a standard, isolated portfolio of all
    LedgerScope domain variables with default test boundaries.
    """
    return {
        # Expenses
        EXPENSE: Expense(expected_value=1000, min_value=500, max_value=2000),
        EXPENSE_MONTHLY_RENT: Rent(min_value=1000, max_value=3000),
        EXPENSE_TRAVEL_FEE: TravelFee(max_value=1500),
        EXPENSE_RENDER_FEE: RenderFee(min_value=1000, max_value=2000),

        # Costs
        COST: Cost(),
        ## Letting it initialize as None/0 protects engine from stale state bugs.
        COST_ADVERTISING: AdvertisingCost(min_value=10000, max_value=30000),
        COST_CPA: CostPerAcquisition(min_value=12, max_value=36),
        COST_CONVERSION_RATE: ConversionRate(min_value=0.04, max_value=0.2),

        # Deals
        REVENUE: 0,
        ## Revenue is a pure output metric of a specific model simulation ($Orders \times Items \times Price$).
        ## It cannot hold static boundaries because it has no standalone existence outside of execution logic.
        ## Leaving it out of the variable portfolio keeps architecture pure.
        DEAL_ORDERS: Orders(min_value=20, max_value=30),
        DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=1, max_value=5),
        DEAL_SELLING_PRICE: SellingPrice(min_value=3000, max_value=6000),
        DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=1000, max_value=2000),

        # Finance
        FINANCE_INTEREST_RATE: InterestRate(expected_value=0.05),
        FINANCE_TAX_RATE: TaxRate(expected_value=0.2),
        FINANCE_USD_TO_RMB: USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5),
    }
