"""
linear_regression_styles.py
Clean design tokens and layout engines for linear regression visualizations.
"""

from matplotlib import cm
from matplotlib.ticker import FuncFormatter

from . import common

# Re-expose common line weight tokens for benchmark lines
LINE_SETTING_BIGGER = common.LINE_SETTING_BIGGER
LINE_SETTING_SMALLER = common.LINE_SETTING_SMALLER

# 1. Canvas Dimensions & Limits
CANVAS_FIGURE_SIZE = (9, 5.5)
POINT_SIZE_MINIMUM = 15
POINT_SIZE_MAXIMUM = 80

# 2. Colors & Palettes
REGRESSION_COLORMAP = cm.viridis_r
GRID_LINE_COLOR = '#dee2e6'
SPINE_BORDER_COLOR = '#dee2e6'

# 3. Component Configuration Maps
TREND_LINE_PROPERTIES = {
    'color': common.COLOR_NAVY,
    'linewidth': 1.5,
    'zorder': 5
}

DATA_POINT_PROPERTIES = {
    'cmap': common.COLOR_SET,
    'edgecolor': 'none',
    'alpha': 0.9,
    'zorder': 3
}

# 4. Typography Hierarchy Configs
TITLE_FONT_CONFIGURATION = common.TITLE_FONT
IN_LEGEND_TEXT_FONTS = common.LEGENDS_TEXT_FONTS

AXIS_LABEL_FONT = {
    'family': 'sans-serif',
    'color': common.X_AXIS_COLOR,
    'fontweight': 'bold',
    'size': 10
}

# 5. Templates & Text Maps
CANVAS_MAIN_TITLE = "Linear Regression Analysis: {y_label} vs {x_label}"
GOAL_BENCHMARK_TEMPLATE = "{label} Benchmark: {benchmark}"
REGRESSION_LINE_DESCRIPTION = "Trend Line ({equation} | $R^2$: {metric:.2f})"


def apply_regression_theme(ax, x_label, y_label, x_formatter, y_formatter):
    """Applies corporate styling tokens to layout boundaries in a single shot."""
    # Headings and Labels
    ax.set_title(CANVAS_MAIN_TITLE.format(x_label=x_label, y_label=y_label), fontdict=TITLE_FONT_CONFIGURATION,
                 loc='center')
    ax.set_xlabel(x_label, fontdict=AXIS_LABEL_FONT)
    ax.set_ylabel(y_label, fontdict=AXIS_LABEL_FONT, labelpad=35, rotation=0, y=0.5)

    # Dynamic Axis Functional Strings Formatting
    ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: x_formatter(val)))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: y_formatter(val)))

    # Tick Parameters Adjustment
    ax.tick_params(axis='x', colors=common.X_AXIS_COLOR, labelsize=9, labelrotation=45)
    ax.tick_params(axis='y', colors=common.Y_AXIS_COLOR, labelsize=9)

    # Muted Background Grid Lines Layout
    ax.grid(True, linestyle='--', linewidth=0.7, color=GRID_LINE_COLOR, alpha=0.7, zorder=1)

    # Spine/Frame Simplification
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_BORDER_COLOR)
        ax.spines[spine].set_linewidth(1)

    # Legend Construction Cleanup
    legend = ax.legend(**IN_LEGEND_TEXT_FONTS)
    legend.get_frame().set_linewidth(1)
