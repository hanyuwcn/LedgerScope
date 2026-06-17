"""
two_way_sensitivity_heatmap_styles.py
Centralized design tokens and layout engines for sensitivity heatmaps.
"""

from . import common_styles

# 1. Visualization Container Metrics
FIGURE_SIZE = common_styles.FIGURE_SIZE
CBAR_SHRINK_RATIO = common_styles.CBAR_SHRINK_RATIO
HEATMAP_CONTEXT = "notebook"
HEATMAP_COLORS = common_styles.COLOR_SET

# 2. Layout Text Templates
HEATMAP_TITLE = "Heatmap of impact of {factor_1} & {factor_2} on {output}"


def scale_font(font_dict, factor):
    new_dict = font_dict.copy()
    if 'size' in new_dict:
        new_dict['size'] *= factor
    return new_dict


def apply_heatmap_theme(ax, ax_heatmap, x_var_name, y_var_name, output_name, x_formatter, y_formatter, title=None,
                        amplify_font=False):
    amp = 2.5 if amplify_font else 1.0

    # 1. Colorbar
    cbar = ax_heatmap.collections[0].colorbar
    cbar.ax.set_title(output_name, fontdict=scale_font(common_styles.X_AXIS_FONT, amp), pad=10 * amp)
    cbar.ax.tick_params(labelsize=common_styles.TICK_SIZE * amp)

    # 2. Main Title and Labels
    ax.set_title(
        title or HEATMAP_TITLE.format(factor_1=x_var_name, factor_2=y_var_name, output=output_name),
        fontdict=scale_font(common_styles.TITLE_FONT, amp),
        pad=common_styles.TITLE_PADDING * amp
    )
    ax.set_xlabel(x_var_name, fontdict=scale_font(common_styles.X_AXIS_FONT, amp))
    ax.set_ylabel(y_var_name, fontdict=scale_font(common_styles.Y_AXIS_FONT, amp),
                  labelpad=common_styles.Y_AXIS_PADDING * amp, rotation=common_styles.Y_AXIS_ROTATION)

    # 3. Formatted Labels
    ax.set_xticklabels([x_formatter(float(l.get_text())) for l in ax.get_xticklabels()])
    ax.set_yticklabels([y_formatter(float(l.get_text())) for l in ax.get_yticklabels()])

    # 4. Ticks
    ax.tick_params(axis='x',
                   colors=common_styles.X_AXIS_COLOR,
                   labelsize=common_styles.TICK_SIZE * amp,
                   labelrotation=common_styles.X_TICK_ROTATION)
    ax.tick_params(axis='y',
                   colors=common_styles.Y_AXIS_COLOR,
                   labelsize=common_styles.TICK_SIZE * amp,
                   labelrotation=common_styles.Y_TICK_ROTATION)
