DYNAMIC_PIPELINE_CONFIGS = {
    # Components
    ## Advertising
    "advertising": [
        "advertising_expense",
        "advertising_efficiency_google_search",

        ### Advertising efficiency
        "cost_per_lead_google_search",
    ],

    ## Selling price
    "selling_price": [
        "deduction_rate",
        "unit_fob",

        "unit_merchant_freight_expense",
        "unit_retail_margin",
        "unit_tariff",

        "currency_exchange",
    ],

    ## Cost of good sold
    "cost_of_goods_sold": [
        "order",
        "units_sold",
        "cogs",
    ],

    ## Expense of selling and management
    "expense": [
        ### Selling
        "brand_freight_expense",
        "selling_expense",

        ### Management
        "monthly_expense",
        "management_expense",

        ### Total expense
        "total_expense",

        ### Expense averaged to each unit
        "unit_fixed_overhead_expense",
        "unit_marketing_expense",

    ],

    ## Finance
    "finance": [
        "depreciation",
        "capital_expenditure",
    ],

    ## Reports from income statements
    ## Including revenue, gross profit, operating income, net income and free cash flow
    "income_reports": [
        "revenue",
        "gross_profit",
        "operating_income",
        "net_income",
        "free_cash_flow",

        ### Income averaged to each unit
        "unit_gross_profit",
        "unit_operating_income",
    ],

    ## Metrics
    "metrics": [
        "cost_per_lead_google_search",
        "roi",
        "cac",
        "roas",
        "market_price",
    ],

    ## Auditors
    "auditors": [
        "deduction_auditor",
        "unit_gross_profit_auditor",
        "unit_operating_income_auditor",
        "freight_expense_auditor",
        "price_architecture_auditor",
    ],

    ## Allocation to units metrics
    "allocation_metrics_pipeline": [
        ### Ads
        "cost_per_lead_google_search",

        ### Expense
        "unit_fixed_overhead_expense",
        "unit_marketing_expense",

        ### Income
        "unit_gross_profit",
        "unit_operating_income",
    ],

    # Aggregated pipelines
    ## From ads, price to final reports
    "end_to_end_pipeline": [
        ## Ads
        "advertising_expense",
        "advertising_efficiency_google_search",

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
    ],

    ## From marketing, price to final reports, including auditors and unit metrics
    ## Including all models
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

        ### Allocation to units
        "unit_gross_profit",
        "unit_operating_income",

        "unit_gross_profit_auditor",
        "unit_operating_income_auditor",

        ## Metrics
        "roi",
        "cac",
        "roas",
        "market_price",

        ## Auditors
        "deduction_auditor",
        "unit_gross_profit_auditor",
        "unit_operating_income_auditor",
        "freight_expense_auditor",
        "price_architecture_auditor",
    ]
}
