from statistics import mean

import matplotlib.colors as mcolors
from matplotlib import cm
from matplotlib.ticker import FuncFormatter

from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt


def get_formatter(var_name):
    """Retrieves the assigned metric lambda, falling back to a clean default."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def get_axis_formatters(output_name):
    """Generates standard functional axis transformation engines."""
    x_formatter = get_formatter(output_name)
    x_axis_formatter = FuncFormatter(lambda x, pos: x_formatter(x))
    y_axis_formatter = FuncFormatter(lambda y, pos: fmt(y, d=2, p=True))

    return x_axis_formatter, y_axis_formatter


def compute_simulation_stats(simulations, output_name):
    """Extracts base telemetry array metrics from the simulation collection."""
    data = [sim[output_name] for sim in simulations]
    return {
        "data": data,
        "min": min(data),
        "max": max(data),
        "mean": mean(data)
    }


def compute_target_percentages(data, goal):
    """Computes target success fractions when a validation threshold is present."""
    if goal is None:
        return None, None

    total = len(data)
    met_count = sum(1 for val in data if val > goal)

    pct_met = (met_count / total) * 100
    pct_not_met = 100 - pct_met
    return pct_met, pct_not_met


def get_gradient_normalizer(data_min, data_max):
    """Creates a color field normalizer with zero-variance crash protections."""
    if data_min != data_max:
        return mcolors.Normalize(data_min, data_max)
    return mcolors.Normalize(data_min - 1, data_max + 1)


def get_threshold_boundary_colors():
    """Extracts structural context colors directly from the core theme map."""
    return {
        "color_not_met": cm.viridis_r(0.25),  # Yellow-Green bounds
        "color_met": cm.viridis_r(0.75)  # Blue-Purple bounds
    }
