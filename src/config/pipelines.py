DYNAMIC_PIPELINE_CONFIGS = {
    # Pipeline Components
    "costs": [
        "advertising_efficiency_google_search",
        "order_model",
        "cogs",
        "total_cost"
    ],

    # Scenario A: Marketing Efficiency Focus
    "marketing_roi_analysis": [
        "advertising_efficiency_google_search",
        "order_model"
        "cogs",
        "total_cost",
        "revenue",
        "profit"
    ],

    # Scenario B: Corporate Capital & Income Focus
    "earnings_and_capex_run": [
        "advertising_efficiency_google_search",
        "cogs",
        "total_cost",
        "revenue",
        "depreciation",
        "capital_expenditure",
        "net_income"
    ],

    # Scenario C: Full Macro Performance
    "complete_macro_metrics": [
        "advertising_efficiency_google_search", "cogs", "revenue", "total_cost",
        "monthly_expense", "total_expense",
        "depreciation", "capital_expenditure",
        "net_income", "profit", "free_cash_flow", "roi"
    ]
}
