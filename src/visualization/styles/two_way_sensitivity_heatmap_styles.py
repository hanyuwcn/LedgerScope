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


def apply_heatmap_theme(ax, ax_heatmap, x_var_name, y_var_name, output_name, x_formatter, y_formatter):
    """Applies corporate styling tokens to layout boundaries in a single shot."""
    # 1. Style the Colorbar Title Context
    cbar = ax_heatmap.collections[0].colorbar
    cbar.ax.set_title(output_name, fontdict=common_styles.X_AXIS_FONT, pad=10)

    # 2. Configure Main Titles and Structural Labels
    ax.set_title(
        HEATMAP_TITLE.format(factor_1=x_var_name, factor_2=y_var_name, output=output_name),
        fontdict=common_styles.TITLE_FONT,
        pad=common_styles.TITLE_PADDING
    )
    ax.set_xlabel(x_var_name, fontdict=common_styles.X_AXIS_FONT)
    ax.set_ylabel(y_var_name, fontdict=common_styles.Y_AXIS_FONT, labelpad=common_styles.Y_AXIS_PADDING,
                  rotation=common_styles.Y_AXIS_ROTATION)

    # 3. Apply Custom Dynamic Map Formatting Rules onto Active Labels Collection
    formatted_x = [x_formatter(float(label.get_text())) for label in ax.get_xticklabels()]
    formatted_y = [y_formatter(float(label.get_text())) for label in ax.get_yticklabels()]
    ax.set_xticklabels(formatted_x)
    ax.set_yticklabels(formatted_y)

    # 4. Refine Ticks and Labels Presentation
    ax.tick_params(axis='x', colors=common_styles.X_AXIS_COLOR, labelsize=common_styles.TICK_SIZE,
                   labelrotation=common_styles.X_TICK_ROTATION)
    ax.tick_params(axis='y', colors=common_styles.Y_AXIS_COLOR, labelsize=common_styles.TICK_SIZE,
                   labelrotation=common_styles.Y_TICK_ROTATION)
