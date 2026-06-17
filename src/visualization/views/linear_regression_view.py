"""
linear_regression_view.py
Calculates stats and renders high-fidelity linear regression plots.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.visualization.styles import linear_regression_styles
from .common_view import get_formatter


def generate_linear_regression_from_lists(x_data, y_data, x_label, y_label,
                                          x_benchmark=None, y_benchmark=None,
                                          ax=None, title=None):
    """
    Generates a high-fidelity linear regression plot styled for the enterprise dashboard.

    This function performs linear regression analysis on the provided data and
    renders a trend line, data points, and optional benchmark lines. It supports
    both standalone rendering and integration into aggregated multi-view layouts.
    Font sizes and layout elements are automatically scaled when utilized in
    aggregated (multi-view) contexts to maintain readability.

    Args:
        x_data (list or np.ndarray): Independent variable data points.
        y_data (list or np.ndarray): Dependent variable data points.
        x_label (str): Label for the x-axis, used for formatting and legend generation.
        y_label (str): Label for the y-axis, used for formatting and legend generation.
        x_benchmark (float, optional): Optional vertical benchmark line coordinate.
            Defaults to None.
        y_benchmark (float, optional): Optional horizontal benchmark line coordinate.
            Defaults to None.
        ax (matplotlib.axes.Axes, optional): A target axes object for aggregation.
            If None, a new figure and axes are created internally. Defaults to None.
        title (str, optional): A custom title for the plot. If None, a default
            title is generated from x_label and y_label. Defaults to None.

    Returns:
        matplotlib.figure.Figure: The Figure object if created internally
            (standalone mode). Returns None if an 'ax' was provided
            (aggregated mode).

    Example:
        >>> # Standalone usage
        >>> fig = generate_linear_regression_from_lists(x_vals, y_vals, "Revenue", "MarketPrice")

        >>> # Aggregated usage with orchestrator
        >>> plot_functions = [lambda ax: generate_linear_regression_from_lists(x_vals, y_vals, "Rev", "Price", ax=ax)]
        >>> fig = plot_multiple_views(plot_functions)
    """
    x, y = np.array(x_data), np.array(y_data)
    b, c, r_value, _, _ = stats.linregress(x, y)
    r_squared = r_value ** 2

    # Ownership logic
    created_new_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=linear_regression_styles.CANVAS_FIGURE_SIZE)
        created_new_fig = True

    x_range = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_range, b * x_range + c,
            label=linear_regression_styles.REGRESSION_LINE_DESCRIPTION.format(
                equation=f"{y_label} = {x_label} * {b:,.2f} {'+' if c >= 0 else '-'} {abs(c):,.2f}",
                metric=r_squared),
            **linear_regression_styles.TREND_LINE_PROPERTIES)

    ax.scatter(x, y, c=x, **linear_regression_styles.DATA_POINT_PROPERTIES)

    # Benchmarks
    x_fmt, y_fmt = get_formatter(x_label), get_formatter(y_label)
    if x_benchmark is not None:
        ax.axvline(x=x_benchmark, label=linear_regression_styles.GOAL_BENCHMARK_TEMPLATE.format(label=x_label,
                                                                                                benchmark=x_fmt(
                                                                                                    x_benchmark)),
                   **linear_regression_styles.LINE_SETTING_BIGGER)
    if y_benchmark is not None:
        ax.axhline(y=y_benchmark, label=linear_regression_styles.GOAL_BENCHMARK_TEMPLATE.format(label=y_label,
                                                                                                benchmark=y_fmt(
                                                                                                    y_benchmark)),
                   **linear_regression_styles.LINE_SETTING_SMALLER)

    # Theme
    linear_regression_styles.apply_regression_theme(
        ax, x_label, y_label, x_fmt, y_fmt,
        title=title, amplify_font=(not created_new_fig)
    )

    if created_new_fig:
        plt.tight_layout()
        return fig
    return None
