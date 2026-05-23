from src.config import settings
from src.engine import evaluate_stochastic_iteration
from src.utils import check_variables_for_function, check_model_pipeline_topology_order


def stochastic_contribution_analysis(
        variables: dict,
        breakdown_metrics: list[str],
        model_pipeline: list,
        shuffled_inputs: list[str],
        sample_size: int = settings.SAMPLE_SIZE
) -> dict[str, float]:
    """
    Executes a Monte Carlo simulation across shuffled parameters to determine the
    average absolute contribution of specified component metrics to an overall cost or revenue pool.

    Args:
        variables (dict): Global project registry mapping variable keys to domain values.
        breakdown_metrics (list[str]): The subset of sub-component metrics forming the pie chart
            boundaries (e.g., ["COGS", "ShippingCost", "MarketingExpenses"]).
        model_pipeline (list): Ordered sequence of core calculation execution blocks.
        shuffled_inputs (list[str]): Subset of variable keys allowed to randomly fluctuate.
        sample_size (int, optional): Total Monte Carlo iterations. Defaults to settings.SAMPLE_SIZE.

    Returns:
        dict[str, float]: Mapping of each breakdown metric to its averaged simulation value.
    """
    # Enforce internal pipeline topological order checks
    check_variables_for_function(variables, shuffled_inputs)
    check_model_pipeline_topology_order(model_pipeline)

    # Initialize tracking container for absolute accumulation
    cumulative_contributions = {metric_name: 0.0 for metric_name in breakdown_metrics}

    # Execute simulation iterations to sample the business layout space
    for _ in range(sample_size):
        runtime_state = evaluate_stochastic_iteration(
            variables=variables,
            shuffled_inputs=shuffled_inputs,
            model_pipeline=model_pipeline
        )

        for metric_name in breakdown_metrics:
            cumulative_contributions[metric_name] += float(runtime_state[metric_name])

    # Reduce cumulative aggregates down to historical statistical means
    average_contributions = {
        metric_name: total_accumulated / sample_size
        for metric_name, total_accumulated in cumulative_contributions.items()
    }

    return average_contributions
