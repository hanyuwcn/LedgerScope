import matplotlib.pyplot as plt
import numpy as np

from src.visualization.styles import contribution_pie_styles
from .common_view import get_formatter


def generate_contribution_pie_chart(average_contributions: dict[str, float], ax=None, title=None) -> plt.Figure:
    """
    Generates a production-grade pie chart styled for the enterprise dashboard.

    This function handles both standalone rendering and integration into aggregated
    multi-view layouts. It provides automatic font scaling for aggregated views
    and customizable titles.

    Args:
        average_contributions (dict[str, float]): A mapping of variable names
            to their calculated mean absolute values (e.g., from a stochastic
            contribution analysis).
        ax (matplotlib.axes.Axes, optional): A target axes object for
            aggregation. If None, a new figure and axes are created.
            Defaults to None.
        title (str, optional): A custom title for the chart. If None, the
            system default pie title is used. Defaults to None.

    Returns:
        plt.Figure: The Figure object if created internally (standalone mode).
            Returns None if an 'ax' was provided (aggregated mode).

    Example:
        >>> # Standalone usage
        >>> fig = generate_contribution_pie_chart(data)

        >>> # Aggregated usage with orchestrator
        >>> plot_functions = [lambda ax: generate_contribution_pie_chart(data, ax=ax)]
        >>> fig = plot_multiple_views(plot_functions)
    """
    labels = list(average_contributions.keys())
    raw_values = np.array(list(average_contributions.values()), dtype=float)
    total_sum = raw_values.sum()
    plot_values = np.full_like(raw_values, 1e-9) if total_sum <= 0.0 else raw_values

    # Determine ownership
    created_new_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=contribution_pie_styles.CANVAS_FIGURE_SIZE)
        created_new_fig = True

    # Amplification logic: True if we are in an aggregated mode
    amp = 3 if not created_new_fig else 1.0

    # Colors
    slice_colors = contribution_pie_styles.PIE_COLORMAP(np.linspace(0.1, 0.9, len(labels))) if len(labels) > 1 else [
        contribution_pie_styles.PIE_COLORMAP(0.5)]

    # Prepare labels
    graph_labels, legend_labels = [], []
    for var_name, val in average_contributions.items():
        formatter = get_formatter(var_name)
        pct = (val / total_sum * 100.0) if total_sum > 0.0 else 0.0
        graph_labels.append(f"{var_name}\n({pct:.1f}%)")
        legend_labels.append(f"{var_name} ({formatter(val)})")

    # Draw Pie
    wedges, texts = ax.pie(
        plot_values,
        labels=graph_labels,
        colors=slice_colors,
        startangle=contribution_pie_styles.PIE_START_ANGLE,
        textprops=contribution_pie_styles.scale_font(contribution_pie_styles.SLICE_TEXT_PROPERTIES, amp),
        wedgeprops=contribution_pie_styles.WEDGE_PROPERTIES
    )

    ax.axis('equal')

    # Apply Title
    ax.set_title(
        title or contribution_pie_styles.PIE_MAIN_TITLE,
        fontdict=contribution_pie_styles.scale_font(contribution_pie_styles.TITLE_FONT_CONFIGURATION, amp),
        pad=20 * amp
    )

    # Legend
    legend_props = contribution_pie_styles.LEGEND_PROPERTIES.copy()
    legend_props.update(contribution_pie_styles.scale_font(legend_props, amp))

    legend = ax.legend(wedges, legend_labels, **legend_props)
    legend.get_frame().set_linewidth(1)

    if created_new_fig:
        fig.tight_layout()
        return fig
    return None
