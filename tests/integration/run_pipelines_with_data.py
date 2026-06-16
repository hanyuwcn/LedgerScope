import random

from src.engine import evaluate_expected_scenario
from src.pipelines import PipelineComposer
from src.utils import check_model_pipeline_topology_order
from tests.fixtures import get_panoramic_variable_portfolio


def sample_model_composition():
    random.seed(20260605)

    end_to_end_pipeline_pipeline = PipelineComposer.build_named_scenario("end_to_end_pipeline")
    panoramic_pipeline = PipelineComposer.build_named_scenario("panoramic_pipeline")

    # print(check_model_pipeline_topology_order(end_to_end_pipeline_pipeline))
    # print(check_model_pipeline_topology_order(panoramic_pipeline))

    panoramic_variables = get_panoramic_variable_portfolio()

    print(evaluate_expected_scenario(variables=panoramic_variables,
                                     model_pipeline=panoramic_pipeline))

    advertising_pipeline = PipelineComposer.build_named_scenario("advertising")
    selling_price_pipeline = PipelineComposer.build_named_scenario("selling_price")
    cost_of_goods_sold_pipeline = PipelineComposer.build_named_scenario("cost_of_goods_sold")
    expense_pipeline = PipelineComposer.build_named_scenario("expense")
    finance_pipeline = PipelineComposer.build_named_scenario("finance")
    income_reports_pipeline = PipelineComposer.build_named_scenario("income_reports")
    metrics_pipeline = PipelineComposer.build_named_scenario("metrics")
    auditors_pipeline = PipelineComposer.build_named_scenario("auditors")
    unit_metrics_pipeline_pipeline = PipelineComposer.build_named_scenario("allocation_metrics_pipeline")

    print(check_model_pipeline_topology_order(advertising_pipeline))
    print(check_model_pipeline_topology_order(selling_price_pipeline))
    print(check_model_pipeline_topology_order(cost_of_goods_sold_pipeline))
    print(check_model_pipeline_topology_order(expense_pipeline))
    print(check_model_pipeline_topology_order(finance_pipeline))
    print(check_model_pipeline_topology_order(income_reports_pipeline))
    print(check_model_pipeline_topology_order(metrics_pipeline))
    print(check_model_pipeline_topology_order(auditors_pipeline))
    print(check_model_pipeline_topology_order(unit_metrics_pipeline_pipeline))

    aggregated_pipeline = PipelineComposer.build_merged_scenarios(["end_to_end_pipeline",
                                                                   "allocation_metrics_pipeline",
                                                                   "auditors",
                                                                   ])
    print(check_model_pipeline_topology_order(aggregated_pipeline))

    print(evaluate_expected_scenario(variables=panoramic_variables,
                                     model_pipeline=aggregated_pipeline))


if __name__ == "__main__":
    sample_model_composition()
