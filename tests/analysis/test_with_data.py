from src.config import variable_names
from src.engine import evaluate_chained_models
from src.models import ProfitModel, CostOfGoodsSoldModel, TotalCostModel, RevenueModel
from src.variables import Orders, SellingPrice, PurchasingPrice, ItemsPerOrder, USDToRMB, AdvertisingCost

if __name__ == "__main__":
    variables = {variable_names.DEAL_ORDERS: Orders(min_value=20, max_value=30),
                 variable_names.DEAL_SELLING_PRICE: SellingPrice(min_value=3000, max_value=6000),
                 variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=1000, max_value=2000),
                 variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=1),
                 variable_names.COST_ADVERTISING: AdvertisingCost(min_value=0, max_value=1000),
                 variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=1, max_value=5)}

    cogs_model = CostOfGoodsSoldModel()
    cost_model = TotalCostModel()
    revenue_model = RevenueModel()
    profit_model = ProfitModel()

    numeric_variables = {variable_names: variable_value.get_value() for variable_names, variable_value in
                         variables.items()}
    cogs_model.input_variables = numeric_variables

    print(
        evaluate_chained_models(numeric_variables, [cogs_model, cost_model]) == {'Orders': 25.0, 'SellingPrice': 4500.0,
                                                                                 'PurchasingPrice': 1500.0,
                                                                                 'USDToRMB': 1,
                                                                                 'AdvertisingCost': 500.0,
                                                                                 'ItemsPerOrder': 3.0, 'Cogs': 112500.0,
                                                                                 'Cost': 113000.0})

    # df = run_two_way_sensitivity_analysis(variables=variables, param_x_name=variable_names.DEAL_ORDERS,
    #                                       param_y_name=variable_names.DEAL_SELLING_PRICE,
    #                                       model_pipeline=[cogs_model, cost_model, revenue_model, profit_model], target_output_name=variable_names.PROFIT,
    #                                       x_steps=30, y_steps=20, reverse_x=False, reverse_y=True)
    # print(df)

    # figure = generate_heatmap_from_df(df, output_name)
    # plt.show()
