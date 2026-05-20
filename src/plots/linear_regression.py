import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import StrMethodFormatter
from scipy import stats

from src.config import plots


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

    # Generate points along the regression line
    x_range = np.linspace(x.min(), x.max(), 100)
    y_trend = b * x_range + c

    # Format the equation string perfectly (y = bx + c)
    sign = "+" if c >= 0 else "-"
    # equation_str = f"Eq: y = {b:,.2f}x {sign} {abs(c):,.2f}"
    equation_str = f"Eq: {y_label} = {x_label} * {b:,.2f} {sign} {abs(c):,.2f}"

    # --- DYNAMIC SIZE SCALING BLOCK ---
    # Safely normalize y-values to a professional display range (15pt to 130pt)
    y_min, y_max = y.min(), y.max()
    if y_max != y_min:
        # Standard Min-Max normalization mapping to [15, 130]
        scaled_sizes = (plots.LINEAR_REGRESSION_POINT_SIZE_MIN +
                        ((y - y_min) / (y_max - y_min)) *
                        (plots.LINEAR_REGRESSION_POINT_SIZE_MAX - plots.LINEAR_REGRESSION_POINT_SIZE_MIN))
    else:
        # Fallback uniform size if all Y values happen to be identical
        scaled_sizes = np.full_like(y, 50, dtype=float)
    # ----------------------------------

    # Set up the figure with clean proportions
    fig, ax = plt.subplots(dpi=100, figsize=plots.LINEAR_REGRESSION_FIGURE_SIZE)

    ## Configure global font styles to match the 'Segoe UI' dashboard theme
    # plt.rcParams['font.family'] = 'sans-serif'
    # plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Tahoma', 'Geneva', 'Arial']

    # 1. Plot trend line (Heavy Blue background color match: #4682B4)
    ax.plot(x_range, y_trend, label=f'Trend Line ({equation_str} | $R^2$: {r_squared:.2f})',
            **plots.LINEAR_REGRESSION_LINE_FORMAT)

    # 2. Scatter actual data points with dynamic "coolwarm" coloring
    scatter_points = ax.scatter(x, y, c=x, s=scaled_sizes, **plots.LINEAR_REGRESSION_POINT_STYLE)

    # 3. Dynamic Benchmarks Plotting (Optional) using Muted Grey (#7F8C8D)
    if x_benchmark is not None:
        ax.axvline(x=x_benchmark,
                   label=plots.LINEAR_REGRESSION_LINE_GOAL.format(label=x_label, benchmark=x_benchmark),
                   **plots.LINE_SETTING_BIGGER
                   )

    if y_benchmark is not None:
        ax.axhline(y=y_benchmark,
                   label=plots.LINEAR_REGRESSION_LINE_GOAL.format(label=y_label, benchmark=y_benchmark),
                   **plots.LINE_SETTING_SMALLER)

    # 4. Clean Dashboard Styling & Grid Rules
    ax.set_title(plots.LINEAR_REGRESSION_TITLE.format(x_label=x_label, y_label=y_label),
                 fontdict=plots.TITLE_FONT,
                 loc='center')

    ax.set_xlabel(x_label,
                  fontdict=plots.LINEAR_REGRESSION_X_AXIS_FONT)

    # Horizontal y-axis title, centered vertically (y=0.5), pushed out slightly (labelpad=35)
    ax.set_ylabel(y_label,
                  fontdict=plots.LINEAR_REGRESSION_Y_AXIS_FONT,
                  labelpad=35, rotation=0, y=0.5)

    # Mute grid lines to match dashboard table borders (#dee2e6)
    ax.grid(True, linestyle='--', linewidth=0.7, color='#dee2e6', alpha=0.7, zorder=1)

    # Simplify borders (spines) - remove top and right frame lines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#dee2e6')
        ax.spines[spine].set_linewidth(1)

    # Format tick parameters
    # ax.tick_params(colors='#6c757d', labelsize=TICK_SIZE)
    ax.tick_params(axis='x', colors=plots.X_AXIS_COLOR, labelsize=plots.LINEAR_REGRESSION_TICK_SIZE, labelrotation=45)
    ax.tick_params(axis='y', colors=plots.Y_AXIS_COLOR, labelsize=plots.LINEAR_REGRESSION_TICK_SIZE)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # 5. Set up elegant, unobtrusive legend matching dashboard cards
    legend = ax.legend(**plots.LINEAR_REGRESSION_IN_LEGENDS_TEXT_FONTS)
    legend.get_frame().set_linewidth(1)

    plt.tight_layout()
    return fig, ax
