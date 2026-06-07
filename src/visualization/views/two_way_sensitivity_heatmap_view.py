"""
two_way_sensitivity_heatmap_view.py
Isolated heatmap engine tied directly to the break-even sensitivity analytics frame.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from src.config import variable_names
from src.visualization.styles import two_way_sensitivity_heatmap_styles
from .common_view import get_formatter


def generate_heatmap_from_df(df, output_name=variable_names.MODEL_DEFAULT_OUTPUT_NAME):
    """
    Generates a high-fidelity 2D sensitivity heatmap from an input DataFrame,
    enforcing explicit axis formatting, type guards, and isolated runtime scopes.
    """
    # 1. Resolve variable labels from DataFrame structural axes
    x_var_name = df.columns.name or "Variable X"
    y_var_name = df.index.name or "Variable Y"

    # 2. Extract corresponding formatting rules dynamically via configuration lookup maps
    output_formatter = get_formatter(output_name)
    x_formatter = get_formatter(x_var_name)
    y_formatter = get_formatter(y_var_name)

    cbar_axis_formatter = FuncFormatter(lambda x, pos: output_formatter(x))

    # 3. Isolate runtime parameters within context configuration sandboxes
    with plt.rc_context():
        sns.set_theme()
        sns.set_context(two_way_sensitivity_heatmap_styles.HEATMAP_CONTEXT)

        fig, ax = plt.subplots(figsize=two_way_sensitivity_heatmap_styles.FIGURE_SIZE, layout="constrained")

        # 4. Generate the base heatmap representation matrix
        ax_heatmap = sns.heatmap(
            df,
            cmap=two_way_sensitivity_heatmap_styles.HEATMAP_COLORS,
            ax=ax,
            cbar_kws={
                'format': cbar_axis_formatter,
                'shrink': two_way_sensitivity_heatmap_styles.CBAR_SHRINK_RATIO
            }
        )

        # 5. Hand off visual theme presentation formatting directly to the styles layer
        two_way_sensitivity_heatmap_styles.apply_heatmap_theme(
            ax=ax,
            ax_heatmap=ax_heatmap,
            x_var_name=x_var_name,
            y_var_name=y_var_name,
            output_name=output_name,
            x_formatter=x_formatter,
            y_formatter=y_formatter
        )

    return fig
