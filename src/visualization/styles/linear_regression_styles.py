"""
linear_regression_styles.py
Clean design tokens and layout engines for linear regression visualizations.
"""

from matplotlib import cm

from . import common_styles

# Re-expose common line weight tokens for benchmark lines
LINE_SETTING_BIGGER = common_styles.LINE_SETTING_BIGGER
LINE_SETTING_SMALLER = common_styles.LINE_SETTING_SMALLER

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
    'color': common_styles.COLOR_NAVY,
    'linewidth': 1.5,
    'zorder': 5
}

DATA_POINT_PROPERTIES = {
    'cmap': common_styles.COLOR_SET,
    'edgecolor': 'none',
    'alpha': 0.9,
    'zorder': 3
}

# 4. Typography Hierarchy Configs
TITLE_FONT_CONFIGURATION = common_styles.TITLE_FONT
IN_LEGEND_TEXT_FONTS = common_styles.LEGENDS_TEXT_FONTS

AXIS_LABEL_FONT = {
    'family': 'sans-serif',
    'color': common_styles.X_AXIS_COLOR,
    'fontweight': 'bold',
    'size': 10
}

# 5. Templates & Text Maps
CANVAS_MAIN_TITLE = "Linear Regression Analysis: {y_label} vs {x_label}"
GOAL_BENCHMARK_TEMPLATE = "{label} Benchmark: {benchmark}"
REGRESSION_LINE_DESCRIPTION = "Trend Line ({equation} | $R^2$: {metric:.2f})"


def scale_font(font_dict, factor):
    return common_styles.scale_font(font_dict, factor)


def apply_regression_theme(ax, x_label, y_label, x_formatter, y_formatter, title=None, amplify_font=False):
    amp = 2.5 if amplify_font else 1.0

    # Titles and Labels
    ax.set_title(title or CANVAS_MAIN_TITLE.format(x_label=x_label, y_label=y_label),
                 fontdict=scale_font(TITLE_FONT_CONFIGURATION, amp), pad=20 * amp)
    ax.set_xlabel(x_label, fontdict=scale_font(AXIS_LABEL_FONT, amp))
    ax.set_ylabel(y_label, fontdict=scale_font(AXIS_LABEL_FONT, amp),
                  labelpad=35 * amp, rotation=0, y=0.5)

    # Ticks
    ax.tick_params(axis='x', labelsize=9 * amp, labelrotation=45)
    ax.tick_params(axis='y', labelsize=9 * amp)

    # Legend
    legend = ax.legend(
        **{**IN_LEGEND_TEXT_FONTS, 'prop': scale_font(IN_LEGEND_TEXT_FONTS.get('prop', {'size': 10}), amp)})
    legend.get_frame().set_linewidth(1)
