from matplotlib import pyplot as plt


def sample_break_even_analysis_plots():
    from src.analysis import break_even_analysis
    from src.config import variable_names
    from src.core import Variable
    from src.models import NetIncomeModel, MarketPriceModel, OperatingIncomeModel
    from src.variables import PriceToEarningsRatio
    from src.visualization import render_break_even_dashboard, get_break_even_dataframe

    variables = {
        variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
        variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
    }

    pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

    break_even_analysis_report = break_even_analysis(variables=variables,
                                                     selected_variables=[variable_names.REVENUE, variable_names.COGS],
                                                     model_pipeline=pipeline,
                                                     output_name=variable_names.MARKET_PRICE,
                                                     goal=5000000.0)

    print(break_even_analysis_report)

    ####

    print(get_break_even_dataframe(break_even_analysis_report, variable_names.MARKET_PRICE))

    ####

    render_break_even_dashboard(break_even_analysis_report, variable_names.MARKET_PRICE)

    ####

    print(break_even_analysis_report)

    ####

    break_even_analysis_report_always_feasible = break_even_analysis(variables=variables,
                                                                     selected_variables=[variable_names.REVENUE,
                                                                                         variable_names.COGS],
                                                                     model_pipeline=pipeline,
                                                                     output_name=variable_names.MARKET_PRICE,
                                                                     goal=4000000.0)

    print(get_break_even_dataframe(break_even_analysis_report_always_feasible, variable_names.MARKET_PRICE))

    ####

    render_break_even_dashboard(break_even_analysis_report_always_feasible, variable_names.MARKET_PRICE)

    ####

    break_even_analysis_report_unreachable = break_even_analysis(variables=variables,
                                                                 selected_variables=[variable_names.REVENUE,
                                                                                     variable_names.COGS],
                                                                 model_pipeline=pipeline,
                                                                 output_name=variable_names.MARKET_PRICE,
                                                                 goal=7000000.0)

    ####

    print(get_break_even_dataframe(break_even_analysis_report_unreachable, variable_names.MARKET_PRICE))

    ####

    render_break_even_dashboard(break_even_analysis_report_unreachable, variable_names.MARKET_PRICE)


def sample_comparative_statics_analysis_plots():
    from src.analysis import comparative_statics
    from src.config import variable_names
    from src.core import Variable
    from src.models import OperatingIncomeModel, NetIncomeModel, MarketPriceModel
    from src.variables import PriceToEarningsRatio
    from src.visualization import get_comparative_statics_dataframe, render_comparative_statics_dashboard

    variables = {
        variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
        variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
    }

    pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

    comparative_statics_reports = comparative_statics(
        variables=variables,
        selected_variables=[variable_names.REVENUE, variable_names.COGS, variable_names.PE_RATIO],
        model_pipeline=pipeline,
        output_name=variable_names.MARKET_PRICE
    )

    print(comparative_statics_reports)

    print(get_comparative_statics_dataframe(comparative_statics_reports, variable_names.GROSS_PROFIT))

    render_comparative_statics_dashboard(comparative_statics_reports, variable_names.MARKET_PRICE)


def sample_linear_regression():
    from matplotlib import pyplot as plt

    from src.analysis import stochastic_bivariate_simulation
    from src.config import variable_names
    from src.core import Variable
    from src.models import OperatingIncomeModel, NetIncomeModel, MarketPriceModel
    from src.variables import PriceToEarningsRatio
    from src.visualization import generate_linear_regression_from_lists

    variables = {
        variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
        variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
    }

    pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

    simulated_x, simulated_y, stats = stochastic_bivariate_simulation(
        variables=variables,
        independent_target_x=variable_names.REVENUE,
        dependent_target_y=variable_names.MARKET_PRICE,
        shuffled_variables=[variable_names.REVENUE],
        model_pipeline=pipeline,
        sample_size=100
    )

    print(stats)

    fig = generate_linear_regression_from_lists(simulated_x, simulated_y,
                                                variable_names.REVENUE, variable_names.MARKET_PRICE)
    plt.show()

    simulated_x, simulated_y, stats = stochastic_bivariate_simulation(
        variables=variables,
        independent_target_x=variable_names.REVENUE,
        dependent_target_y=variable_names.MARKET_PRICE,
        shuffled_variables=[variable_names.REVENUE, variable_names.COGS],
        model_pipeline=pipeline,
        sample_size=100
    )

    fig = generate_linear_regression_from_lists(simulated_x, simulated_y,
                                                variable_names.REVENUE, variable_names.MARKET_PRICE)
    plt.show()

    fig = generate_linear_regression_from_lists(simulated_x, simulated_y,
                                                variable_names.REVENUE, variable_names.MARKET_PRICE,
                                                x_benchmark=100000, y_benchmark=5000000)
    plt.show()

    plt.close()


def sample_simulation_analysis():
    from matplotlib import pyplot as plt

    from src.analysis import run_monte_carlo
    from src.config import variable_names
    from src.core import Variable
    from src.models import OperatingIncomeModel, NetIncomeModel, MarketPriceModel
    from src.variables import PriceToEarningsRatio
    from src.visualization import generate_histogram_from_array

    variables = {
        variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
        variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
    }

    pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

    monte_carlo_simulation_report = run_monte_carlo(
        variables=variables,
        shuffled_inputs=[variable_names.REVENUE, variable_names.COGS, variable_names.PE_RATIO],
        model_pipeline=pipeline,
        iterations=50
    )

    # print(monte_carlo_simulation_report)

    generate_histogram_from_array(monte_carlo_simulation_report, variable_names.MARKET_PRICE)
    plt.show()

    generate_histogram_from_array(monte_carlo_simulation_report, variable_names.MARKET_PRICE, goal=10000000)
    plt.show()

    generate_histogram_from_array(monte_carlo_simulation_report, variable_names.MARKET_PRICE, goal=6000000)
    plt.show()

    plt.close()


def sample_two_variables_sensitivity_analysis():
    from matplotlib import pyplot as plt

    from src.analysis import run_two_way_sensitivity_analysis
    from src.config import variable_names
    from src.core import Variable
    from src.models import OperatingIncomeModel, NetIncomeModel, MarketPriceModel
    from src.variables import PriceToEarningsRatio
    from src.visualization import generate_heatmap_from_df

    variables = {
        variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
        variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
    }

    pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

    two_way_sensitivity_analysis_report = run_two_way_sensitivity_analysis(
        variables=variables,
        param_x_name=variable_names.REVENUE,
        param_y_name=variable_names.COGS,
        model_pipeline=pipeline,
        target_output_name=variable_names.MARKET_PRICE,
        x_steps=20,
        y_steps=20
    )

    # print(two_way_sensitivity_analysis_report)

    figure = generate_heatmap_from_df(two_way_sensitivity_analysis_report, variable_names.MARKET_PRICE)
    plt.show()

    two_way_sensitivity_analysis_cost_decreasing_report = run_two_way_sensitivity_analysis(
        variables=variables,
        param_x_name=variable_names.REVENUE,
        param_y_name=variable_names.COGS,
        model_pipeline=pipeline,
        target_output_name=variable_names.MARKET_PRICE,
        reverse_y=False,
        x_steps=20,
        y_steps=20
    )

    figure = generate_heatmap_from_df(two_way_sensitivity_analysis_cost_decreasing_report, variable_names.MARKET_PRICE)
    plt.show()

    plt.close()


def sample_contribution_analysis():
    from src.analysis import stochastic_contribution_analysis
    from src.config import variable_names
    from src.core import Variable
    from src.models import OperatingIncomeModel, NetIncomeModel, MarketPriceModel
    from src.variables import PriceToEarningsRatio
    from src.visualization import generate_contribution_pie_chart

    variables = {
        variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
        variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
        variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
    }

    pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

    breakdown = [variable_names.REVENUE, variable_names.COGS]
    shuffled = [variable_names.REVENUE, variable_names.COGS]

    contribution_analysis_report = stochastic_contribution_analysis(
        variables=variables,
        breakdown_metrics=breakdown,
        model_pipeline=pipeline,
        shuffled_inputs=shuffled,
        sample_size=100
    )

    print(contribution_analysis_report)

    generate_contribution_pie_chart(contribution_analysis_report)

    plt.show()
    plt.close()


if __name__ == "__main__":
    pass
    # sample_break_even_analysis_plots()
    # sample_comparative_statics_analysis_plots()
    # sample_contribution_analysis()
    # sample_linear_regression()
    # sample_simulation_analysis()
    # sample_two_variables_sensitivity_analysis()
