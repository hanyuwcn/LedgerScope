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
    ],

    "panoramic_pipeline": [
        ## Ads
        "advertising_expense",
        "advertising_efficiency_google_search",

        "cost_per_lead_google_search",

        ## Merchant
        "deduction_rate",
        "unit_fob",

        "unit_merchant_freight_expense",
        "unit_retail_margin",
        "unit_tariff",

        "currency_exchange",

        ## Brand
        "order",
        "units_sold",
        "cogs",

        ## Expense
        #### Selling
        "brand_freight_expense",
        "selling_expense",

        #### Management
        "monthly_expense",
        "management_expense",

        "unit_fixed_overhead_expense",
        "unit_marketing_expense",

        "total_expense",

        ## Finance
        "depreciation",
        "capital_expenditure",

        ## Income
        "revenue",
        "gross_profit",
        "operating_income",
        "net_income",
        "free_cash_flow",

        "unit_gross_profit",
        "unit_operating_income",

        ## Metrics
        "roi",
        "cac",
        "roas",
        "market_price",
    ],

    "panoramic_with_auditor_pipeline": [
        ## Ads
        "advertising_expense",
        "advertising_efficiency_google_search",

        "cost_per_lead_google_search",

        ## Merchant
        "deduction_rate",
        "unit_fob",

        "unit_merchant_freight_expense",
        "unit_retail_margin",
        "unit_tariff",

        "currency_exchange",

        ## Brand
        "order",
        "units_sold",
        "cogs",

        ## Expense
        #### Selling
        "brand_freight_expense",
        "selling_expense",

        #### Management
        "monthly_expense",
        "management_expense",

        "unit_fixed_overhead_expense",
        "unit_marketing_expense",

        "total_expense",

        ## Finance
        "depreciation",
        "capital_expenditure",

        ## Income
        "revenue",
        "gross_profit",
        "operating_income",
        "net_income",
        "free_cash_flow",

        "unit_gross_profit",
        "unit_operating_income",

        "unit_gross_profit_auditor",
        "unit_operating_income_auditor",

        ## Metrics
        "roi",
        "cac",
        "roas",
        "market_price",

        ## UnitsMetrics
        # "cost_per_lead_google_search",
        # "unit_merchant_freight_expense",
        # "unit_retail_margin",
        # "unit_tariff",
        # "unit_fixed_overhead_expense",
        # "unit_marketing_expense",
        # "unit_gross_profit",
        # "unit_operating_income",

        ## Auditors
        "deduction_auditor",
        "unit_gross_profit_auditor",
        "unit_operating_income_auditor",
        "freight_expense_auditor",
        "price_architecture_auditor",
    ]
}
