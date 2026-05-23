import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy import stats

from src.config import plots  # For baseline line settings
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
# Relative import structure referencing the partner style sheet
from .linear_regression_styles import (
    GRID_LINE_COLOR,
    SPINE_BORDER_COLOR,
    TREND_LINE_PROPERTIES,
    DATA_POINT_PROPERTIES,
    TITLE_FONT_CONFIGURATION,
    X_AXIS_LABEL_FONT,
    Y_AXIS_LABEL_FONT,
    IN_LEGEND_TEXT_FONTS,
    Y_AXIS_LABEL_PAD,
    Y_AXIS_LABEL_ROTATION,
    Y_AXIS_LABEL_Y_CENTER,
    X_AXIS_TICK_ROTATION,
    CANVAS_FIGURE_SIZE,
    POINT_SIZE_MINIMUM,
    POINT_SIZE_MAXIMUM,
    X_AXIS_TICK_SIZE,
    Y_AXIS_TICK_SIZE,
    CANVAS_MAIN_TITLE,
    GOAL_BENCHMARK_TEMPLATE,
    X_AXIS_COLOR_RULE,
    Y_AXIS_COLOR_RULE
)


def _get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def generate_linear_regression_from_lists(x_data, y_data, x_label, y_label, x_benchmark=None, y_benchmark=None):
    """
    Generates a production-grade linear regression plot styled to match
    the enterprise dashboard aesthetic, featuring centered headers, vertical
    y-axis layouts, and smaller borderless gradient data points.
    """
    # Convert inputs to numpy arrays just in case lists were passed
    x = np.array(x_data)
    y = np.array(y_data)

    # Calculate the linear regression line properties
    b, c, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value ** 2

    # --- ZERO-VARIANCE SAFETY GUARD FOR X-AXIS LINSPACE ---
    x_min, x_max = x.min(), x.max()
    if x_min != x_max:
        x_range = np.linspace(x_min, x_max, 100)
    else:
        # Expand boundaries by 1 unit if all X values happen to be identical
        x_range = np.linspace(x_min - 1, x_max + 1, 100)

    # Generate points along the regression line
    y_trend = b * x_range + c

    # Format the equation string perfectly (y = bx + c)
    sign = "+" if c >= 0 else "-"
    equation_str = f"Eq: {y_label} = {x_label} * {b:,.2f} {sign} {abs(c):,.2f}"

    # --- ZERO-VARIANCE SAFETY GUARD FOR Y-AXIS SIZING ---
    y_min, y_max = y.min(), y.max()
    if y_max != y_min:
        # Standard Min-Max normalization mapping to config bounds
        scaled_sizes = (POINT_SIZE_MINIMUM +
                        ((y - y_min) / (y_max - y_min)) *
                        (POINT_SIZE_MAXIMUM - POINT_SIZE_MINIMUM))
    else:
        # Fallback uniform size if all Y values happen to be identical
        scaled_sizes = np.full_like(y, 50, dtype=float)

    # Isolate global style elements dynamically using context configuration sandboxes
    with plt.rc_context():
        fig, ax = plt.subplots(dpi=100, figsize=CANVAS_FIGURE_SIZE)

        # 1. Plot trend line
        ax.plot(x_range, y_trend, label=f'Trend Line ({equation_str} | $R^2$: {r_squared:.2f})',
                **TREND_LINE_PROPERTIES)

        # 2. Scatter actual data points relying entirely on style sheet unpacked mappings
        scatter_points = ax.scatter(
            x, y,
            c=x,
            s=scaled_sizes,
            **DATA_POINT_PROPERTIES
        )

        # 3. Dynamic Benchmarks Plotting (Optional) using Muted Grey
        if x_benchmark is not None:
            ax.axvline(x=x_benchmark,
                       label=GOAL_BENCHMARK_TEMPLATE.format(label=x_label, benchmark=x_benchmark),
                       **plots.LINE_SETTING_BIGGER)

        if y_benchmark is not None:
            ax.axhline(y=y_benchmark,
                       label=GOAL_BENCHMARK_TEMPLATE.format(label=y_label, benchmark=y_benchmark),
                       **plots.LINE_SETTING_SMALLER)

        # 4. Clean Dashboard Styling & Grid Rules
        ax.set_title(CANVAS_MAIN_TITLE.format(x_label=x_label, y_label=y_label),
                     fontdict=TITLE_FONT_CONFIGURATION,
                     loc='center')

        ax.set_xlabel(x_label, fontdict=X_AXIS_LABEL_FONT)

        # Horizontal y-axis title, centered vertically, pushed out via padding
        ax.set_ylabel(y_label,
                      fontdict=Y_AXIS_LABEL_FONT,
                      labelpad=Y_AXIS_LABEL_PAD,
                      rotation=Y_AXIS_LABEL_ROTATION,
                      y=Y_AXIS_LABEL_Y_CENTER)

        # Mute grid lines to match dashboard table borders
        ax.grid(True, linestyle='--', linewidth=0.7, color=GRID_LINE_COLOR, alpha=0.7, zorder=1)

        # Simplify borders (spines) - remove top and right frame lines
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        for spine in ['left', 'bottom']:
            ax.spines[spine].set_color(SPINE_BORDER_COLOR)
            ax.spines[spine].set_linewidth(1)

        # 5. Format tick parameters and apply dynamic axis formatters
        ax.tick_params(axis='x', colors=X_AXIS_COLOR_RULE, labelsize=X_AXIS_TICK_SIZE,
                       labelrotation=X_AXIS_TICK_ROTATION)
        ax.tick_params(axis='y', colors=Y_AXIS_COLOR_RULE, labelsize=Y_AXIS_TICK_SIZE)

        # Resolve x and y custom format rules dynamically via map lookup
        x_formatter = _get_formatter(x_label)
        y_formatter = _get_formatter(y_label)

        ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: x_formatter(val)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: y_formatter(val)))

        # 6. Set up elegant, unobtrusive legend matching dashboard cards
        legend = ax.legend(**IN_LEGEND_TEXT_FONTS)
        legend.get_frame().set_linewidth(1)

        plt.tight_layout()

        # Object is returned alive so Jupyter can fetch and render it exactly once.
        return fig
