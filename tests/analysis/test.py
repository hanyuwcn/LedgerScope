from src.analysis import break_even_analysis
from src.config import variable_names
from src.models import PipelineComposer
from src.variables import Orders, SellingPrice, PurchasingPrice, ItemsPerOrder, USDToRMB, CostPerAcquisition, \
    ConversionRate, AdvertisingCost, Expense
from src.visualization import get_break_even_dataframe

if __name__ == "__main__":
    # cogs_model = CostOfGoodsSoldModel()
    # cost_model = TotalCostModel()
    # revenue_model = RevenueModel()
    # expense_model = TotalExpenseModel()
    # depreciation_model = DepreciationModel()
    # capital_expenditure_model = CapitalExpenditureModel()
    # net_income_model = NetIncomeModel()
    # advertising_efficiency_model = AdvertisingEfficiencyModel()
    # free_cash_flow_model = FreeCashFlowModel()
    # profit_model = ProfitModel()
    # roi_model = RoiModel()

    advertising_budget = AdvertisingCost(min_value=10000, max_value=30000)
    orders = Orders(min_value=20, max_value=30)
    usd_to_rmb = USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5)
    selling_price = SellingPrice(min_value=3000, max_value=6000)
    items_per_order = ItemsPerOrder(min_value=1, max_value=5)
    purchasing_price = PurchasingPrice(min_value=1000, max_value=2000)
    conversion_rate = ConversionRate(min_value=0.04, max_value=0.2)
    cpa = CostPerAcquisition(min_value=12, max_value=36)
    expense = Expense(0)

    # variables = {variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
    #              variable_names.DEAL_ORDERS: orders,
    #              variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
    #              variable_names.COST_ADVERTISING: advertising_budget,
    #              variable_names.COST_CONVERSION_RATE: conversion_rate,
    #              variable_names.COST_CPA: cpa,
    #              variable_names.DEAL_SELLING_PRICE: selling_price,
    #              variable_names.DEAL_ITEMS_PER_ORDER: items_per_order}

    # expected_result = evaluate_expected_scenario(variables=variables,
    #                                              model_pipeline=[advertising_efficiency_model, cogs_model,
    #                                                              revenue_model, cost_model, expense_model,
    #                                                              depreciation_model, net_income_model,
    #                                                              capital_expenditure_model, profit_model])
    #
    # simulated_x_distribution, simulated_y_distribution, linear_trend_summary = stochastic_bivariate_simulation(
    #     variables=variables,
    #     independent_target_x=variable_names.PROFIT,
    #     dependent_target_y=variable_names.ROI,
    #     shuffled_variables=[variable_names.DEAL_ORDERS,
    #                         variable_names.DEAL_SELLING_PRICE,
    #                         variable_names.DEAL_ITEMS_PER_ORDER],
    #     model_pipeline=[cogs_model, revenue_model, cost_model, expense_model,
    #                     depreciation_model, net_income_model,
    #                     capital_expenditure_model, profit_model, roi_model],
    #     sample_size=3)
    #
    # # print(linear_trend_summary)
    # print(simulated_x_distribution)
    # print(simulated_y_distribution)

    # fig = generate_linear_regression_from_lists(simulated_x_distribution, simulated_y_distribution,
    #                                             variable_names.PROFIT, variable_names.ROI,
    #                                             x_benchmark=20000, y_benchmark=20)
    # plt.show()

    # fig = generate_linear_regression_from_lists([1417453.884662906, 3638045.6308474177, 1087920.967565786],
    #                                             [16.518141165932597, 17.876111541317844, 13.627810201670274],
    #                                             "Profit", "ROI",
    #                                             x_benchmark=2000000, y_benchmark=17)
    # plt.show()

    # variables_2 = {variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
    #                variable_names.DEAL_SELLING_PRICE: selling_price,
    #                variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
    #                variable_names.DEAL_ITEMS_PER_ORDER: items_per_order,
    #                variable_names.COST_ADVERTISING: advertising_budget,
    #                variable_names.COST_CPA: cpa,
    #                variable_names.COST_CONVERSION_RATE: conversion_rate,
    #                variable_names.EXPENSE: expense}
    #
    # simulated_x_distribution, simulated_y_distribution, linear_trend_summary = stochastic_bivariate_simulation(
    #     variables=variables_2,
    #     independent_target_x=variable_names.COST_ADVERTISING,
    #     dependent_target_y=variable_names.NET_INCOME,
    #     shuffled_variables=[
    #         variable_names.COST_ADVERTISING,
    #         variable_names.DEAL_SELLING_PRICE,
    #         variable_names.DEAL_ITEMS_PER_ORDER],
    #     model_pipeline=[advertising_efficiency_model, cogs_model, revenue_model, cost_model,
    #                     depreciation_model, capital_expenditure_model,
    #                     net_income_model, profit_model, roi_model],
    #     sample_size=100)
    #
    # fig = generate_linear_regression_from_lists(simulated_x_distribution, simulated_y_distribution,
    #                                             variable_names.COST_ADVERTISING, variable_names.NET_INCOME,
    #                                             x_benchmark=20000, y_benchmark=2000000)
    # plt.show()

    variables = {variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=1, max_value=5),
                 variable_names.DEAL_ORDERS: Orders(min_value=20, max_value=30),
                 variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5),
                 variable_names.COST_ADVERTISING: AdvertisingCost(min_value=10000, max_value=30000),
                 variable_names.COST_CPA: CostPerAcquisition(min_value=12, max_value=36),
                 variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.04, max_value=0.2),
                 variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=1000, max_value=2000),
                 variable_names.DEAL_SELLING_PRICE: SellingPrice(min_value=3000, max_value=6000)}

    # Case A: Execute the baseline standard template
    base_pipeline = PipelineComposer.build_named_scenario("marketing_roi_analysis")

    # Case B: Execute the template with your requested Free Cash Flow add-on!
    marketing_fcf_pipeline = PipelineComposer.build_named_scenario(
        "marketing_roi_analysis",
        "free_cash_flow"
    )

    # Case C: Go fully complex by stacking multiple custom modular mixins on the fly
    advanced_pipeline = PipelineComposer.build_named_scenario(
        "marketing_roi_analysis",
        "free_cash_flow",
        "depreciation",
        "capital_expenditure"
    )

    print(base_pipeline)
    print(marketing_fcf_pipeline)
    print(advanced_pipeline)

    break_even_analysis_report = break_even_analysis(variables, selected_variables=[variable_names.DEAL_ORDERS,
                                                                                    variable_names.DEAL_SELLING_PRICE],
                                                     model_pipeline=base_pipeline,
                                                     output_name=variable_names.PROFIT, goal=0)

    print(get_break_even_dataframe(break_even_analysis_report, variable_names.PROFIT))
