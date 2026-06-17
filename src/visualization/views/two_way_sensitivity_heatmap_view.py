import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from src.config import variable_names
from src.visualization.styles import two_way_sensitivity_heatmap_styles
from .common_view import get_formatter


def generate_heatmap_from_df(df, output_name=variable_names.MODEL_DEFAULT_OUTPUT_NAME, ax=None, title=None):
    """
    Generates a high-fidelity 2D sensitivity heatmap from an input DataFrame.

    This function is context-aware: it can generate a standalone figure if no
    axes are provided, or render directly into a pre-allocated axes object for
    use in aggregated multi-view reports. It automatically applies font
    scaling to maintain readability when utilized in constrained (aggregated) layouts.

    Args:
        df (pd.DataFrame): A DataFrame where the index and columns represent
            variable sensitivity ranges, and values represent the model output.
        output_name (str, optional): The label for the output metric being
            analyzed. Defaults to the system default model output name.
        ax (matplotlib.axes.Axes, optional): A target axes object for
            aggregation. If None, a new figure and axes are created
            internally. Defaults to None.
        title (str, optional): A custom title for the heatmap. If None,
            a default title is generated describing the sensitivity relationship.
            Defaults to None.

    Returns:
        matplotlib.figure.Figure: The Figure object if created internally
            (standalone mode). Returns None if an 'ax' was provided
            (aggregated mode).

    Example:
        >>> # Standalone usage
        >>> fig = generate_heatmap_from_df(sensitivity_df, output_name="Valuation")

        >>> # Aggregated usage with orchestrator
        >>> plot_functions = [lambda ax: generate_heatmap_from_df(sensitivity_df, ax=ax)]
        >>> fig = plot_multiple_views(plot_functions)
    """
    if df.empty:
        fig, ax_internal = plt.subplots()
        ax_internal.text(0.5, 0.5, "No data available", ha='center', va='center')
        return fig

    # 1. Setup Ownership
    created_new_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=two_way_sensitivity_heatmap_styles.FIGURE_SIZE, layout="constrained")
        created_new_fig = True

    # 2. Logic Prep
    x_var_name, y_var_name = df.columns.name or "Variable X", df.index.name or "Variable Y"
    cbar_axis_formatter = FuncFormatter(lambda x, pos: get_formatter(output_name)(x))

    # 3. Render Heatmap
    ax_heatmap = sns.heatmap(
        df,
        cmap=two_way_sensitivity_heatmap_styles.HEATMAP_COLORS,
        ax=ax,
        cbar_kws={'format': cbar_axis_formatter, 'shrink': two_way_sensitivity_heatmap_styles.CBAR_SHRINK_RATIO}
    )

    # 4. Styling
    two_way_sensitivity_heatmap_styles.apply_heatmap_theme(
        ax=ax,
        ax_heatmap=ax_heatmap,
        x_var_name=x_var_name,
        y_var_name=y_var_name,
        output_name=output_name,
        x_formatter=get_formatter(x_var_name),
        y_formatter=get_formatter(y_var_name),
        title=title,
        amplify_font=(not created_new_fig)
    )

    if created_new_fig:
        return fig
    return None
