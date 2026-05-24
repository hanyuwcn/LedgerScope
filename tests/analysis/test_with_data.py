from matplotlib import pyplot as plt

from src.analysis import break_even_analysis, comparative_statics, stochastic_bivariate_simulation, run_monte_carlo, \
    run_two_way_sensitivity_analysis, stochastic_contribution_analysis
from src.config import variable_names
from src.engine import evaluate_chained_models, evaluate_variable_scenario_sweep
from src.models import ProfitModel, CostOfGoodsSoldModel, RevenueModel, FreeCashFlowModel, \
    CapitalExpenditureModel, DepreciationModel, TotalExpenseModel, NetIncomeModel, RoiModel, TotalCostModel, \
    AdvertisingEfficiencyModel
from src.variables import (Orders, SellingPrice, PurchasingPrice, ItemsPerOrder, USDToRMB, Rent, TaxRate,
                           CostPerAcquisition, ConversionRate, RenderFee, TravelFee, AdvertisingCost, Expense)
from src.visualization import render_break_even_dashboard, generate_heatmap_from_df, generate_histogram_from_array, \
    generate_linear_regression_from_lists, render_comparative_statics_dashboard, get_break_even_dataframe


### New approach

def sample_analysis():
    orders = Orders(min_value=20, max_value=30)
    usd_to_rmb = USDToRMB(expected_value=1)
    selling_price = SellingPrice(min_value=3000, max_value=6000)
    items_per_order = ItemsPerOrder(min_value=1, max_value=5)
    purchasing_price = PurchasingPrice(min_value=1000, max_value=2000)
    rent = Rent(min_value=1000, max_value=2000)
    tax_rate = TaxRate()

    cpa = CostPerAcquisition(min_value=12, max_value=36)
    conversion_rate = ConversionRate(min_value=0.04, max_value=0.2)
    render_fee = RenderFee(expected_value=600, min_value=500, max_value=800)
    travel_fee = TravelFee(min_value=400, max_value=1000)

    variables = {variable_names.DEAL_PURCHASING_PRICE: purchasing_price.get_value(),
                 variable_names.DEAL_ORDERS: orders.get_value(),
                 variable_names.FINANCE_USD_TO_RMB: usd_to_rmb.get_value(),
                 variable_names.DEAL_SELLING_PRICE: selling_price.get_value(),
                 variable_names.DEAL_ITEMS_PER_ORDER: items_per_order.get_value(),
                 variable_names.EXPENSE_MONTHLY_RENT: rent.get_value(),
                 variable_names.FINANCE_TAX_RATE: tax_rate.get_value()}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    free_cash_flow_model = FreeCashFlowModel()
    roi_model = RoiModel()
    profit_model = ProfitModel()

    print(evaluate_chained_models(variables,
                                  [cogs_model, revenue_model, cost_model, expense_model, depreciation_model,
                                   net_income_model,
                                   capital_expenditure_model, free_cash_flow_model])[variable_names.FREE_CASH_FLOW])

    variables[variable_names.EXPENSE_RENDER_FEE] = render_fee.get_value()
    variables[variable_names.EXPENSE_TRAVEL_FEE] = travel_fee.get_value()

    print(evaluate_chained_models(variables,
                                  [cogs_model, revenue_model, cost_model, expense_model, depreciation_model,
                                   net_income_model,
                                   capital_expenditure_model, free_cash_flow_model])[variable_names.FREE_CASH_FLOW])

    # variables[variable_names.COST_CPA] = cpa.get_value()
    # variables[variable_names.COST_CONVERSION_RATE] = conversion_rate.get_value()

    primitive_variables = {variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
                           variable_names.DEAL_ORDERS: orders,
                           variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
                           variable_names.DEAL_SELLING_PRICE: selling_price,
                           variable_names.DEAL_ITEMS_PER_ORDER: items_per_order,
                           variable_names.EXPENSE_MONTHLY_RENT: rent,
                           variable_names.FINANCE_TAX_RATE: tax_rate,
                           variable_names.EXPENSE_RENDER_FEE: render_fee,
                           variable_names.EXPENSE_TRAVEL_FEE: travel_fee
                           }
    item_per_order_range = items_per_order.get_range_values(5)
    # print(item_per_order_range)
    scenario_result = evaluate_variable_scenario_sweep(primitive_variables, variable_names.DEAL_ITEMS_PER_ORDER,
                                                       item_per_order_range,
                                                       [cogs_model, revenue_model, cost_model, expense_model,
                                                        depreciation_model,
                                                        net_income_model,
                                                        capital_expenditure_model, free_cash_flow_model])
    fcf_result = [scenario[variable_names.FREE_CASH_FLOW] for scenario in scenario_result]
    print(fcf_result)


def sample_break_even_analysis_plots():
    variables = {variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=1, max_value=5),
                 variable_names.DEAL_ORDERS: Orders(min_value=20, max_value=30),
                 variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5),
                 variable_names.COST_ADVERTISING: AdvertisingCost(min_value=10000, max_value=30000),
                 variable_names.COST_CPA: CostPerAcquisition(min_value=12, max_value=36),
                 variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.04, max_value=0.2),
                 variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=1000, max_value=2000),
                 variable_names.DEAL_SELLING_PRICE: SellingPrice(min_value=3000, max_value=6000)}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    profit_model = ProfitModel()
    advertising_efficiency_model = AdvertisingEfficiencyModel()

    # print(evaluate_expected_scenario(variables, [advertising_efficiency_model]))

    break_even_analysis_report = break_even_analysis(variables, selected_variables=[variable_names.DEAL_ORDERS,
                                                                                    variable_names.DEAL_SELLING_PRICE],
                                                     model_pipeline=[advertising_efficiency_model,
                                                                     cogs_model, revenue_model, cost_model,
                                                                     expense_model,
                                                                     depreciation_model, net_income_model,
                                                                     capital_expenditure_model, profit_model],
                                                     output_name=variable_names.PROFIT, goal=0)

    print(get_break_even_dataframe(break_even_analysis_report, variable_names.PROFIT))
    # render_break_even_dashboard(break_even_analysis_report, variable_names.PROFIT)
    #
    # break_even_analysis_report_higher_goal = break_even_analysis(variables,
    #                                                              selected_variables=[variable_names.DEAL_ORDERS,
    #                                                                                  variable_names.DEAL_SELLING_PRICE],
    #                                                              model_pipeline=[advertising_efficiency_model,
    #                                                                              cogs_model, revenue_model, cost_model,
    #                                                                              expense_model,
    #                                                                              depreciation_model, net_income_model,
    #                                                                              capital_expenditure_model,
    #                                                                              profit_model],
    #                                                              output_name=variable_names.PROFIT, goal=250000)
    # # print(break_even_analysis_report_higher_goal)
    # render_break_even_dashboard(break_even_analysis_report_higher_goal, variable_names.PROFIT)
    #
    # break_even_analysis_report_highest_goal = break_even_analysis(variables,
    #                                                              selected_variables=[variable_names.DEAL_PURCHASING_PRICE,
    #                                                                                  variable_names.DEAL_SELLING_PRICE,
    #                                                                                  variable_names.DEAL_ORDERS,
    #                                                                                  variable_names.COST_CPA,
    #                                                                                  variable_names.COST_CONVERSION_RATE,
    #                                                                                  variable_names.DEAL_ITEMS_PER_ORDER],
    #                                                              model_pipeline=[advertising_efficiency_model,
    #                                                                              cogs_model, revenue_model, cost_model,
    #                                                                              expense_model,
    #                                                                              depreciation_model, net_income_model,
    #                                                                              capital_expenditure_model,
    #                                                                              profit_model],
    #                                                              output_name=variable_names.PROFIT, goal=250000)
    # # print(break_even_analysis_report_highest_goal)
    # render_break_even_dashboard(break_even_analysis_report_highest_goal, variable_names.PROFIT)

    # Display the dashboard inside your notebook execution runner
    render_break_even_dashboard(break_even_analysis_report, "FreeCashFlow")


def sample_comparative_statics_analysis_plots():
    variables = {variable_names.DEAL_ORDERS: Orders(min_value=20, max_value=30),
                 # variable_names.COST_CPA: CostPerAcquisition(min_value=12, max_value=36),
                 # variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.04, max_value=0.2)
                 variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=1000, max_value=2000),
                 variable_names.DEAL_SELLING_PRICE: SellingPrice(min_value=3000, max_value=6000),
                 variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=1, max_value=5)}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    profit_model = ProfitModel()

    analysis = comparative_statics(variables=variables,
                                   selected_variables=[variable_names.DEAL_ORDERS,
                                                       variable_names.DEAL_SELLING_PRICE,
                                                       variable_names.DEAL_PURCHASING_PRICE],
                                   model_pipeline=[cogs_model, revenue_model, cost_model, expense_model,
                                                   depreciation_model, net_income_model,
                                                   capital_expenditure_model, profit_model],
                                   output_name=variable_names.PROFIT)

    print(analysis)
    render_comparative_statics_dashboard(analysis, variable_names.PROFIT)
    plt.show()


def sample_linear_regression():
    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    advertising_efficiency_model = AdvertisingEfficiencyModel()
    free_cash_flow_model = FreeCashFlowModel()
    profit_model = ProfitModel()
    roi_model = RoiModel()

    advertising_budget = AdvertisingCost(min_value=10000, max_value=30000)
    orders = Orders(min_value=20, max_value=30)
    usd_to_rmb = USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5)
    selling_price = SellingPrice(min_value=3000, max_value=6000)
    items_per_order = ItemsPerOrder(min_value=1, max_value=5)
    purchasing_price = PurchasingPrice(min_value=1000, max_value=2000)
    conversion_rate = ConversionRate(min_value=0.04, max_value=0.2)
    cpa = CostPerAcquisition(min_value=12, max_value=36)
    expense = Expense(0)

    variables = {variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
                 variable_names.DEAL_ORDERS: orders,
                 variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
                 variable_names.COST_ADVERTISING: advertising_budget,
                 variable_names.COST_CONVERSION_RATE: conversion_rate,
                 variable_names.COST_CPA: cpa,
                 variable_names.DEAL_SELLING_PRICE: selling_price,
                 variable_names.DEAL_ITEMS_PER_ORDER: items_per_order}

    # expected_result = evaluate_expected_scenario(variables=variables, model_pipeline=[advertising_efficiency_model, cogs_model,
    #                                                                 revenue_model, cost_model, expense_model,
    #                                                                 depreciation_model, net_income_model,
    #                                                                 capital_expenditure_model, profit_model])
    # print(expected_result[variable_names.PROFIT])

    # expected_result = evaluate_expected_scenario(variables=variables,
    #                                              model_pipeline=[cogs_model,
    #                                                              revenue_model, cost_model, advertising_efficiency_model, expense_model,
    #                                                              depreciation_model, net_income_model,
    #                                                              capital_expenditure_model, profit_model])

    # Model topology error below:
    # stochastic_bivariate_simulation(
    #     variables=variables,
    #     independent_target_x=variable_names.PROFIT,
    #     dependent_target_y=variable_names.ROI,
    #     shuffled_variables=[variable_names.DEAL_ORDERS,
    #                         variable_names.DEAL_SELLING_PRICE,
    #                         variable_names.DEAL_ITEMS_PER_ORDER],
    #     model_pipeline=[cogs_model,
    #                     revenue_model, cost_model,
    #                     advertising_efficiency_model, expense_model,
    #                     depreciation_model, net_income_model,
    #                     capital_expenditure_model, profit_model],
    #     sample_size=100)

    simulated_x_distribution, simulated_y_distribution, linear_trend_summary = stochastic_bivariate_simulation(
        variables=variables,
        independent_target_x=variable_names.PROFIT,
        dependent_target_y=variable_names.ROI,
        shuffled_variables=[variable_names.COST_ADVERTISING,
                            variable_names.DEAL_SELLING_PRICE,
                            variable_names.DEAL_PURCHASING_PRICE,
                            variable_names.COST_CPA,
                            variable_names.COST_CONVERSION_RATE,
                            variable_names.DEAL_ITEMS_PER_ORDER],
        model_pipeline=[advertising_efficiency_model, cogs_model, revenue_model, cost_model, expense_model,
                        depreciation_model, net_income_model,
                        capital_expenditure_model, profit_model, roi_model],
        sample_size=200)

    # print(linear_trend_summary)
    # fig = generate_linear_regression_from_lists(simulated_x_distribution, simulated_y_distribution,
    #                                                variable_names.PROFIT, variable_names.ROI,
    #                                                x_benchmark=2000000, y_benchmark=2)
    # plt.show()

    variables_2 = {variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
                   variable_names.DEAL_SELLING_PRICE: selling_price,
                   variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
                   variable_names.DEAL_ITEMS_PER_ORDER: items_per_order,
                   variable_names.COST_ADVERTISING: advertising_budget,
                   variable_names.COST_CPA: cpa,
                   variable_names.COST_CONVERSION_RATE: conversion_rate,
                   variable_names.EXPENSE: expense}

    simulated_x_distribution, simulated_y_distribution, linear_trend_summary = stochastic_bivariate_simulation(
        variables=variables_2,
        independent_target_x=variable_names.COST_ADVERTISING,
        dependent_target_y=variable_names.NET_INCOME,
        shuffled_variables=[
            variable_names.COST_ADVERTISING,
            variable_names.DEAL_SELLING_PRICE,
            variable_names.DEAL_ITEMS_PER_ORDER],
        model_pipeline=[advertising_efficiency_model, cogs_model, revenue_model, cost_model,
                        depreciation_model, capital_expenditure_model,
                        net_income_model, profit_model, roi_model],
        sample_size=100)

    print(linear_trend_summary)
    fig = generate_linear_regression_from_lists(simulated_x_distribution, simulated_y_distribution,
                                                variable_names.COST_ADVERTISING, variable_names.NET_INCOME,
                                                x_benchmark=20000)
    plt.show()


def sample_two_variables_sensitivity_analysis():
    advertising_budget = AdvertisingCost(min_value=10000, max_value=30000)
    orders = Orders(min_value=20, max_value=30)
    usd_to_rmb = USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5)
    selling_price = SellingPrice(min_value=3000, max_value=6000)
    items_per_order = ItemsPerOrder(min_value=1, max_value=5)
    purchasing_price = PurchasingPrice(min_value=1000, max_value=2000)
    conversion_rate = ConversionRate(min_value=0.04, max_value=0.2)
    cpa = CostPerAcquisition(min_value=12, max_value=36)

    variables = {variable_names.DEAL_ORDERS: orders,
                 variable_names.COST_ADVERTISING: advertising_budget,
                 variable_names.COST_CPA: cpa,
                 variable_names.COST_CONVERSION_RATE: conversion_rate,
                 variable_names.DEAL_SELLING_PRICE: selling_price,
                 variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
                 variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
                 variable_names.DEAL_ITEMS_PER_ORDER: items_per_order}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    advertising_efficiency_model = AdvertisingEfficiencyModel()
    # free_cash_flow_model = FreeCashFlowModel()
    profit_model = ProfitModel()
    # roi_model = RoiModel()

    # two_way_analysis_df = run_two_way_sensitivity_analysis({variable_names.DEAL_ORDERS: orders,
    #              variable_names.COST_ADVERTISING: advertising_budget,
    #              variable_names.COST_CPA: cpa,
    #              variable_names.COST_CONVERSION_RATE: conversion_rate,
    #              variable_names.DEAL_SELLING_PRICE: selling_price,
    #              variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
    #              variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
    #              variable_names.DEAL_ITEMS_PER_ORDER: items_per_order},
    #                                                        param_x_name=variable_names.DEAL_ORDERS,
    #                                                        param_y_name=variable_names.DEAL_SELLING_PRICE,
    #                                                        model_pipeline=[
    #                                                                        cogs_model, revenue_model, cost_model,
    #                                                                        expense_model,
    #                                                                        depreciation_model, net_income_model,
    #                                                                        capital_expenditure_model, profit_model],
    #                                                        target_output_name=variable_names.PROFIT,
    #                                                        x_steps=5, y_steps=3)
    two_way_analysis_df = run_two_way_sensitivity_analysis(variables, param_x_name=variable_names.COST_ADVERTISING,
                                                           param_y_name=variable_names.DEAL_SELLING_PRICE,
                                                           model_pipeline=[advertising_efficiency_model,
                                                                           cogs_model, revenue_model, cost_model,
                                                                           expense_model,
                                                                           depreciation_model, net_income_model,
                                                                           capital_expenditure_model, profit_model],
                                                           target_output_name=variable_names.PROFIT,
                                                           x_steps=30, y_steps=20)
    print(two_way_analysis_df)

    figure = generate_heatmap_from_df(two_way_analysis_df, variable_names.PROFIT)
    plt.show()


def sample_simulation_analysis():
    orders = Orders(min_value=20, max_value=30)
    usd_to_rmb = USDToRMB(expected_value=1)
    selling_price = SellingPrice(min_value=3000, max_value=6000)
    items_per_order = ItemsPerOrder(min_value=1, max_value=5)
    purchasing_price = PurchasingPrice(min_value=1000, max_value=2000)

    variables = {variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
                 variable_names.DEAL_ORDERS: orders,
                 variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
                 variable_names.DEAL_SELLING_PRICE: selling_price,
                 variable_names.DEAL_ITEMS_PER_ORDER: items_per_order}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    # advertising_efficiency_model = AdvertisingEfficiencyModel()
    # free_cash_flow_model = FreeCashFlowModel()
    profit_model = ProfitModel()

    simulations = run_monte_carlo(variables, [variable_names.DEAL_PURCHASING_PRICE,
                                              variable_names.DEAL_SELLING_PRICE],
                                  [cogs_model, revenue_model, cost_model, expense_model, depreciation_model,
                                   capital_expenditure_model, profit_model],
                                  tracked_outputs=[variable_names.PROFIT],
                                  iterations=50)

    # generate_histogram_from_array(simulations, variable_names.PROFIT)
    # plt.show()

    benchmark_goal = 200000
    generate_histogram_from_array(simulations, variable_names.PROFIT, benchmark_goal)
    plt.show()


def sample_contribution_analysis():
    advertising_budget = AdvertisingCost(min_value=10000, max_value=30000)
    orders = Orders(min_value=20, max_value=30)
    usd_to_rmb = USDToRMB(expected_value=6.8, min_value=6.0, max_value=7.5)
    selling_price = SellingPrice(min_value=3000, max_value=6000)
    items_per_order = ItemsPerOrder(min_value=1, max_value=5)
    purchasing_price = PurchasingPrice(min_value=1000, max_value=2000)
    conversion_rate = ConversionRate(min_value=0.04, max_value=0.2)
    cpa = CostPerAcquisition(min_value=12, max_value=36)

    variables = {variable_names.DEAL_ORDERS: orders,
                 variable_names.COST_ADVERTISING: advertising_budget,
                 variable_names.COST_CPA: cpa,
                 variable_names.COST_CONVERSION_RATE: conversion_rate,
                 variable_names.DEAL_SELLING_PRICE: selling_price,
                 variable_names.DEAL_PURCHASING_PRICE: purchasing_price,
                 variable_names.FINANCE_USD_TO_RMB: usd_to_rmb,
                 variable_names.DEAL_ITEMS_PER_ORDER: items_per_order}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    expense_model = TotalExpenseModel()
    depreciation_model = DepreciationModel()
    capital_expenditure_model = CapitalExpenditureModel()
    net_income_model = NetIncomeModel()
    # advertising_efficiency_model = AdvertisingEfficiencyModel()
    # free_cash_flow_model = FreeCashFlowModel()
    profit_model = ProfitModel()

    contributions = stochastic_contribution_analysis(variables=variables,
                                                     breakdown_metrics=[variable_names.COST_ADVERTISING,
                                                                        variable_names.COST_COGS],
                                                     model_pipeline=[cogs_model, revenue_model, cost_model,
                                                                     expense_model, depreciation_model,
                                                                     capital_expenditure_model, profit_model],
                                                     shuffled_inputs=[variable_names.DEAL_PURCHASING_PRICE,
                                                                      variable_names.DEAL_SELLING_PRICE,
                                                                      variable_names.COST_ADVERTISING,
                                                                      variable_names.COST_CONVERSION_RATE,
                                                                      variable_names.COST_CPA],
                                                     sample_size=100)
    print(contributions)

    from src.visualization import generate_contribution_pie_chart

    fig = generate_contribution_pie_chart(contributions)
    plt.show()


def model_aggregation_pipeline():
    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    profit_model = ProfitModel()

    print([cogs_model, cost_model, revenue_model, profit_model])
    print(CostOfGoodsSoldModel.__new__())


if __name__ == "__main__":
    # sample_analysis()
    sample_break_even_analysis_plots()
    # sample_comparative_statics_analysis_plots()
    # sample_two_variables_sensitivity_analysis()
    # sample_linear_regression()
    # sample_simulation_analysis()
    # sample_contribution_analysis()

    # model_aggregation_pipeline()
