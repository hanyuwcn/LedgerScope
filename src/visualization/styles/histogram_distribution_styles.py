"""
histogram_distribution_styles.py
Aesthetic tokens and presentation engines for distribution visualizations.
"""

import matplotlib.colors as mcolors
from matplotlib import cm
from matplotlib.ticker import FuncFormatter

from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from . import common_styles

# Re-expose common core tokens
TITLE_FONT = common_styles.TITLE_FONT
X_AXIS_COLOR = common_styles.X_AXIS_COLOR
Y_AXIS_COLOR = common_styles.Y_AXIS_COLOR
X_AXIS_FONT = common_styles.X_AXIS_FONT
Y_AXIS_FONT = common_styles.Y_AXIS_FONT
FIGURE_SIZE = common_styles.FIGURE_SIZE
TICK_SIZE = common_styles.TICK_SIZE
LINE_SETTING_SMALLER = common_styles.LINE_SETTING_SMALLER
LINE_SETTING_BIGGER = common_styles.LINE_SETTING_BIGGER

# Label contexts
HISTOGRAM_TITLE_CONTEXT = "Distribution of Simulated Density Gradient of {output}"
HISTOGRAM_X_LABEL_CONTEXT = "Simulated Values of {output}"
HISTOGRAM_Y_LABEL_CONTEXT = "Frequency(%)"
HISTOGRAM_VERTICAL_LINE_GOAL = "Benchmark Goal: {goal}"
HISTOGRAM_VERTICAL_LINE_MEAN = 'Simulations Mean: {mean}'

# Component specific configurations
HISTOGRAM_BIN_FONT = {
    'bins': 40,
    'alpha': 0.8,
    'edgecolor': 'white',
    'linewidth': 0.5
}
HISTOGRAM_IN_GRAPH_TEXT_FONTS = {'ha': 'center', 'weight': 'bold', 'family': 'serif'}
HISTOGRAM_IN_LEGENDS_TEXT_FONTS = {
    'loc': 'upper left',
    'bbox_to_anchor': (0.02, 0.88),
    'prop': {'family': 'serif', 'size': 10},
    'frameon': True,
    'facecolor': 'white',
    'edgecolor': common_styles.COLOR_DARK
}


def get_formatter(var_name):
    """Retrieves the assigned metric lambda, falling back to a clean default."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def get_axis_formatters(output_name):
    """Generates functional formatters mapped to column metrics."""
    x_formatter = get_formatter(output_name)
    return (
        FuncFormatter(lambda x, pos: x_formatter(x)),
        FuncFormatter(lambda y, pos: fmt(y, d=2, p=True))
    )


def get_gradient_normalizer(data_min, data_max):
    """Creates a color field normalizer with zero-variance protections."""
    if data_min != data_max:
        return mcolors.Normalize(data_min, data_max)
    return mcolors.Normalize(data_min - 1, data_max + 1)


def get_threshold_boundary_colors():
    """Extracts structural context colors directly from the colormap."""
    return {
        "color_not_met": cm.viridis_r(0.25),
        "color_met": cm.viridis_r(0.75)
    }


def apply_histogram_theme(ax, output_name, title=None, amplify_font=False):
    """Applies corporate styling with optional title and font amplification."""

    # 2.5x is the fixed multiplier for aggregated views
    amp = 2.5 if amplify_font else 1.0

    # Apply scaling to the legend property dictionary
    legend_props = HISTOGRAM_IN_LEGENDS_TEXT_FONTS.copy()
    legend_props['prop'] = common_styles.scale_font(legend_props['prop'], amp)

    ax.legend(**legend_props)

    ax.set_title(
        label=title or HISTOGRAM_TITLE_CONTEXT.format(output=output_name),
        fontdict=common_styles.scale_font(TITLE_FONT, amp),
        pad=50 * amp
    )

    # Bind structural axis formatters
    x_fmt, y_fmt = get_axis_formatters(output_name)
    ax.xaxis.set_major_formatter(x_fmt)
    ax.yaxis.set_major_formatter(y_fmt)

    ax.set_xlabel(HISTOGRAM_X_LABEL_CONTEXT.format(output=output_name),
                  fontdict=common_styles.scale_font(X_AXIS_FONT, amp))
    ax.set_ylabel(HISTOGRAM_Y_LABEL_CONTEXT,
                  fontdict=common_styles.scale_font(Y_AXIS_FONT, amp), rotation=0, labelpad=60 * amp)

    ax.tick_params(axis='x', colors=X_AXIS_COLOR, labelsize=TICK_SIZE * amp, labelrotation=45)
    ax.tick_params(axis='y', colors=Y_AXIS_COLOR, labelsize=TICK_SIZE * amp)
