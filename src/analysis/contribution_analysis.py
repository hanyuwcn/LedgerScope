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
    average absolute contribution of specified component metrics to an overall pool.

    This function performs a dynamic topology check on the model pipeline and
    defensively validates that the runtime output contains all requested breakdown
    metrics during the initial simulation iteration.

    Args:
        variables (dict): Global project registry mapping variable keys to domain values.
        breakdown_metrics (list[str]): The subset of sub-component metrics forming the
            aggregation boundaries.
        model_pipeline (list): Ordered sequence of core calculation execution blocks.
        shuffled_inputs (list[str]): Subset of variable keys allowed to randomly fluctuate.
        sample_size (int, optional): Total Monte Carlo iterations.

    Returns:
        dict[str, float]: Mapping of each breakdown metric to its averaged simulation value.

    Raises:
        KeyError: If the simulation fails to produce any of the required `breakdown_metrics`.
    """
    # 1. Enforce internal pipeline topological order checks
    check_variables_for_function(variables, shuffled_inputs)
    check_model_pipeline_topology_order(model_pipeline)

    # 2. Execute first iteration to validate output contract
    runtime_state = evaluate_stochastic_iteration(
        variables=variables,
        shuffled_inputs=shuffled_inputs,
        model_pipeline=model_pipeline
    )
    check_variables_for_function(runtime_state, breakdown_metrics)

    # 3. Initialize tracking container
    cumulative_contributions = {metric: float(runtime_state[metric]) for metric in breakdown_metrics}

    # 4. Execute remaining simulation iterations
    for _ in range(sample_size - 1):
        runtime_state = evaluate_stochastic_iteration(
            variables=variables,
            shuffled_inputs=shuffled_inputs,
            model_pipeline=model_pipeline
        )
        for metric in breakdown_metrics:
            cumulative_contributions[metric] += float(runtime_state[metric])

    # 5. Reduce to historical statistical means
    return {
        metric: total / sample_size
        for metric, total in cumulative_contributions.items()
    }
