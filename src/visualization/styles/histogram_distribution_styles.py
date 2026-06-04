"""
histogram_distribution_styles.py
Aesthetic tokens and presentation engines for distribution visualizations.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
from matplotlib.ticker import FuncFormatter

from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from . import common

# Re-expose common core tokens
TITLE_FONT = common.TITLE_FONT
X_AXIS_COLOR = common.X_AXIS_COLOR
Y_AXIS_COLOR = common.Y_AXIS_COLOR
X_AXIS_FONT = common.X_AXIS_FONT
Y_AXIS_FONT = common.Y_AXIS_FONT
FIGURE_SIZE = common.FIGURE_SIZE
TICK_SIZE = common.TICK_SIZE
LINE_SETTING_SMALLER = common.LINE_SETTING_SMALLER
LINE_SETTING_BIGGER = common.LINE_SETTING_BIGGER

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
    'edgecolor': common.COLOR_DARK
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


def apply_histogram_theme(ax, output_name):
    """Applies corporate styling tokens to layout boundaries in one shot."""
    # Apply legends and main titles
    ax.legend(**HISTOGRAM_IN_LEGENDS_TEXT_FONTS)
    ax.set_title(
        label=HISTOGRAM_TITLE_CONTEXT.format(output=output_name),
        fontdict=TITLE_FONT,
        pad=50
    )

    # Bind structural axis formatters
    x_fmt, y_fmt = get_axis_formatters(output_name)
    ax.xaxis.set_major_formatter(x_fmt)
    ax.yaxis.set_major_formatter(y_fmt)

    # Clean tick labels
    ax.tick_params(axis='x', colors=X_AXIS_COLOR, labelsize=TICK_SIZE, labelrotation=45)
    ax.tick_params(axis='y', colors=Y_AXIS_COLOR, labelsize=TICK_SIZE)

    # Set structural labels
    ax.set_xlabel(xlabel=HISTOGRAM_X_LABEL_CONTEXT.format(output=output_name), fontdict=X_AXIS_FONT)
    ax.set_ylabel(ylabel=HISTOGRAM_Y_LABEL_CONTEXT, fontdict=Y_AXIS_FONT, rotation=0, labelpad=60)
