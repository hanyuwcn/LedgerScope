DYNAMIC_PIPELINE_CONFIGS = {
    # Pipeline Components
    "costs": [
        "advertising_efficiency_google_search",
        "order_model",
        "cogs",
        "expense",
    ],

    # Scenario A: Marketing Efficiency Focus
    "marketing_roi_analysis": [
        "advertising_efficiency_google_search",
        "order_model"
        "cogs",
        "expense",
        "revenue",
        "profit"
    ],

    # Scenario B: Corporate Capital & Income Focus
    "earnings_and_capex_run": [
        "advertising_efficiency_google_search",
        "cogs",
        "expense",
        "revenue",
        "depreciation",
        "capital_expenditure",
        "net_income"
    ],

    # Scenario C: Full Macro Performance
    "complete_macro_metrics": [
        "advertising_efficiency_google_search", "cogs", "revenue",
        "monthly_expense", "expense",
        "depreciation", "capital_expenditure",
        "net_income", "profit", "free_cash_flow", "roi"
    ]
}
