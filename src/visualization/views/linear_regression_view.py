"""
linear_regression_view.py
Calculates stats and renders high-fidelity linear regression plots.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.visualization.styles import linear_regression_styles
from .common_view import get_formatter


def generate_linear_regression_from_lists(x_data, y_data, x_label, y_label, x_benchmark=None, y_benchmark=None):
    """
    Generates a production-grade linear regression plot styled to match
    the enterprise dashboard aesthetic, featuring centered headers and gradient data points.
    """
    x = np.array(x_data)
    y = np.array(y_data)

    # 1. Compute Linear Regression Coefficients Matrix
    b, c, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value ** 2

    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Zero-variance safety checks
    x_range = np.linspace(x_min, x_max, 100) if x_min != x_max else np.linspace(x_min - 1, x_max + 1, 100)
    y_trend = b * x_range + c

    sign = "+" if c >= 0 else "-"
    equation_str = f"Eq: {y_label} = {x_label} * {b:,.2f} {sign} {abs(c):,.2f}"

    if y_max != y_min:
        scaled_sizes = (linear_regression_styles.POINT_SIZE_MINIMUM +
                        ((y - y_min) / (y_max - y_min)) *
                        (linear_regression_styles.POINT_SIZE_MAXIMUM - linear_regression_styles.POINT_SIZE_MINIMUM))
    else:
        scaled_sizes = np.full_like(y, 50, dtype=float)

    # Dynamic formatters
    x_formatter = get_formatter(x_label)
    y_formatter = get_formatter(y_label)

    # 2. Isolate global style contexts safely
    with plt.rc_context():
        fig, ax = plt.subplots(dpi=100, figsize=linear_regression_styles.CANVAS_FIGURE_SIZE)

        # Draw the regression line
        ax.plot(x_range, y_trend,
                label=linear_regression_styles.REGRESSION_LINE_DESCRIPTION.format(equation=equation_str,
                                                                                  metric=r_squared),
                **linear_regression_styles.TREND_LINE_PROPERTIES)

        # Scatter data points
        ax.scatter(x, y, c=x, s=scaled_sizes, **linear_regression_styles.DATA_POINT_PROPERTIES)

        # Plot benchmarks if present
        if x_benchmark is not None:
            ax.axvline(x=x_benchmark,
                       label=linear_regression_styles.GOAL_BENCHMARK_TEMPLATE.format(
                           label=x_label, benchmark=x_formatter(x_benchmark)),
                       **linear_regression_styles.LINE_SETTING_BIGGER)

        if y_benchmark is not None:
            ax.axhline(y=y_benchmark,
                       label=linear_regression_styles.GOAL_BENCHMARK_TEMPLATE.format(
                           label=y_label, benchmark=y_formatter(y_benchmark)),
                       **linear_regression_styles.LINE_SETTING_SMALLER)

        # 3. Dynamic Viewport Stretching Guard Block
        current_xlim_min, current_xlim_max = ax.get_xlim()
        if x_benchmark is not None:
            offset = abs(x_max - x_min) * 0.1 if x_max != x_min else 1000
            ax.set_xlim(min(current_xlim_min, x_benchmark - offset), max(current_xlim_max, x_benchmark + offset))

        current_ylim_min, current_ylim_max = ax.get_ylim()
        if y_benchmark is not None:
            offset = abs(y_max - y_min) * 0.1 if y_max != y_min else 1
            ax.set_ylim(min(current_ylim_min, y_benchmark - offset), max(current_ylim_max, y_benchmark + offset))

        # 4. Delegate Visual Formatting Styles Execution to Theme Layer
        linear_regression_styles.apply_regression_theme(ax, x_label, y_label, x_formatter, y_formatter)

        plt.tight_layout()
        return fig
