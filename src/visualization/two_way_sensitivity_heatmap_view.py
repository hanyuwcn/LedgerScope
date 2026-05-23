"""
two_way_sensitivity_heatmap_view.py
Isolated heatmap engine tied directly to the break-even sensitivity analytics frame.
"""
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from src.config import variable_names, plots
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from .two_way_sensitivity_heatmap_styles import HEATMAP_LABEL_PROPERTIES


def _get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def generate_heatmap_from_df(df, output_name=variable_names.MODEL_DEFAULT_OUTPUT_NAME):
    """
    Generates a high-fidelity 2D sensitivity heatmap from an input DataFrame,
    enforcing explicit axis formatting, type guards, and isolated runtime scopes.
    """
    # 1. Resolve variable names from the DataFrame schema layout
    x_var_name = df.columns.name or "ConversionRate"
    y_var_name = df.index.name or "FixedKPI"

    # 2. Extract corresponding configuration formatters directly from your dict map
    output_formatter = _get_formatter(output_name)
    x_formatter = _get_formatter(x_var_name)
    y_formatter = _get_formatter(y_var_name)

    # 3. Create explicit FuncFormatters for Matplotlib's layout engines
    cbar_axis_formatter = FuncFormatter(lambda x, pos: output_formatter(x))

    with plt.rc_context():
        sns.set_theme()
        sns.set_context(plots.HEATMAP_CONTEXT)

        fig, ax = plt.subplots(figsize=plots.FIGURE_SIZE, layout="constrained")

        # Generate heatmap configuration matrix
        ax_heatmap = sns.heatmap(
            df,
            annot=False,
            fmt=plots.ROUNDING_FORMAT,
            cmap=plots.HEATMAP_COLORS,
            ax=ax,
            cbar_kws={
                'format': cbar_axis_formatter,
                'shrink': plots.CBAR_SHRINK_RATIO
            }
        )

        cbar = ax_heatmap.collections[0].colorbar
        cbar.ax.set_title(
            output_name,
            fontdict=plots.X_AXIS_FONT,
            pad=10
        )

        ax.set_xlabel(x_var_name, fontdict=plots.X_AXIS_FONT)
        ax.set_ylabel(
            y_var_name,
            rotation=HEATMAP_LABEL_PROPERTIES["y_axis_rotation"],
            labelpad=HEATMAP_LABEL_PROPERTIES["y_axis_padding"],
            fontdict=plots.Y_AXIS_FONT
        )
        ax.set_title(
            plots.HEATMAP_TITLE.format(
                factor_1=x_var_name,
                factor_2=y_var_name,
                output=output_name
            ),
            fontdict=plots.TITLE_FONT,
            pad=HEATMAP_LABEL_PROPERTIES["title_padding"]
        )

        formatted_x_labels = [x_formatter(label.get_text()) for label in ax.get_xticklabels()]
        formatted_y_labels = [y_formatter(label.get_text()) for label in ax.get_yticklabels()]

        ax.set_xticklabels(formatted_x_labels)
        ax.set_yticklabels(formatted_y_labels)

        ax.tick_params(
            axis='x',
            colors=plots.X_AXIS_COLOR,
            labelsize=plots.TICK_SIZE,
            labelrotation=HEATMAP_LABEL_PROPERTIES["x_tick_rotation"]
        )
        ax.tick_params(
            axis='y',
            colors=plots.Y_AXIS_COLOR,
            labelsize=plots.TICK_SIZE,
            labelrotation=HEATMAP_LABEL_PROPERTIES["y_tick_rotation"]
        )

    return fig
