import numpy as np
from scipy import stats

from src.config import settings
from src.engine import evaluate_stochastic_iteration
from src.utils import check_variables_for_function, check_model_pipeline_topology_order


def stochastic_bivariate_simulation(
        variables: dict,
        independent_target_x: str,
        dependent_target_y: str,
        shuffled_variables: list[str],
        model_pipeline: list,
        sample_size: int = settings.SAMPLE_SIZE
) -> tuple[list[float], list[float], dict]:
    """
    Executes a Monte Carlo simulation across shuffled pipeline parameters to generate
    a bivariate dataset for two specific target metrics, computing their linear OLS trend.

    This function acts as a stochastic data generator, simulating operational risks
    to provide the exact data structures needed for downstream scatter plotting,
    distribution mapping, and correlation tracking.

    Args:
        variables (dict): The complete global project registry mapping variable
            identifier keys to their corresponding domain value objects.
        independent_target_x (str): The identifier key of the variable assigned to
            the independent X-axis dataset array.
        dependent_target_y (str): The identifier key of the variable assigned to
            the dependent Y-axis dataset array.
        shuffled_variables (list[str]): Subset of variable keys allowed to randomly
            vary across their distribution ranges during each iteration.
        model_pipeline (list): Ordered sequence of core calculation execution blocks.
        sample_size (int, optional): Total Monte Carlo iterations to execute.
            Defaults to settings.SAMPLE_SIZE.

    Returns:
        tuple[list[float], list[float], dict]: A triplet payload containing:
            1. Raw distribution list of simulated values for the independent X parameter.
            2. Raw distribution list of simulated values for the dependent Y parameter.
            3. Dict containing ordinary least squares (OLS) linear trend metrics.
    """
    check_variables_for_function(variables, shuffled_variables)
    check_model_pipeline_topology_order(model_pipeline)

    simulated_x_distribution = []
    simulated_y_distribution = []

    # Execute Monte Carlo iterations to populate bivariate dataset arrays
    for _ in range(sample_size):
        runtime_state = evaluate_stochastic_iteration(
            variables=variables,
            shuffled_inputs=shuffled_variables,
            model_pipeline=model_pipeline
        )
        simulated_x_distribution.append(runtime_state[independent_target_x])
        simulated_y_distribution.append(runtime_state[dependent_target_y])

    # Run linear trend post-analysis over generated datasets
    linear_trend_summary = _analyze_linear_trend_properties(
        x_values=simulated_x_distribution,
        y_values=simulated_y_distribution,
        x_label=independent_target_x,
        y_label=dependent_target_y
    )

    return simulated_x_distribution, simulated_y_distribution, linear_trend_summary


def _analyze_linear_trend_properties(x_values: list[float], y_values: list[float], x_label: str, y_label: str) -> dict:
    """
    Calculates the Ordinary Least Squares (OLS) regression line properties for the
    generated bivariate distributions.
    """
    if np.var(x_values) == 0.0 or np.var(y_values) == 0.0:
        raise ValueError(
            f"Cannot calculate linear trend line. Simulated coordinate vectors for "
            f"'{x_label}' or '{y_label}' exhibit zero statistical variance."
        )

    slope, intercept, r_value, p_value, std_err = stats.linregress(x=x_values, y=y_values)

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r_squared": float(r_value ** 2),
        "p_value": float(p_value),
        "standard_error": float(std_err)
    }
