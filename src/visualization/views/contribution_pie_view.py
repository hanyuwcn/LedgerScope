import matplotlib.pyplot as plt
import numpy as np

from src.visualization.styles import contribution_pie_styles
from .common_view import get_formatter


def generate_contribution_pie_chart(average_contributions: dict[str, float]) -> plt.Figure:
    """
    Generates a production-grade pie chart styled to match the enterprise dashboard
    aesthetic. Keeps variable names and percentage markers on the graph slices,
    and places the variable names along with their formatted absolute values inside the legend.

    Args:
        average_contributions (dict[str, float]): Output from stochastic_contribution_analysis,
            mapping variable names to their calculated mean absolute values.

    Returns:
        plt.Figure: The standalone Matplotlib figure object isolated via context sandboxing.
    """
    labels = list(average_contributions.keys())
    raw_values = np.array(list(average_contributions.values()), dtype=float)

    total_sum = raw_values.sum()

    # --- ZERO-SUM SAFETY GUARD ---
    if total_sum <= 0.0:
        plot_values = np.full_like(raw_values, 1e-9)
    else:
        plot_values = raw_values

    # Derive balanced discrete colors along the spectrum
    if len(labels) > 1:
        slice_colors = contribution_pie_styles.PIE_COLORMAP(np.linspace(0.1, 0.9, len(labels)))
    else:
        slice_colors = [contribution_pie_styles.PIE_COLORMAP(0.5)]

    graph_labels = []
    legend_labels = []

    for var_name, val in average_contributions.items():
        formatter = get_formatter(var_name)
        formatted_val = formatter(val)

        # Calculate percentage safely from division by zero errors
        pct = (val / total_sum * 100.0) if total_sum > 0.0 else 0.0

        graph_labels.append(f"{var_name}\n({pct:.1f}%)")
        legend_labels.append(f"{var_name} ({formatted_val})")

    # Isolate global style contexts to eliminate downstream side-effects
    with plt.rc_context():
        fig, ax = plt.subplots(dpi=100, figsize=contribution_pie_styles.CANVAS_FIGURE_SIZE)

        # Fixed: Style properties are now clean variable calls sourced from the style file
        wedges, texts = ax.pie(
            plot_values,
            labels=graph_labels,
            colors=slice_colors,
            startangle=contribution_pie_styles.PIE_START_ANGLE,
            textprops=contribution_pie_styles.SLICE_TEXT_PROPERTIES,
            wedgeprops=contribution_pie_styles.WEDGE_PROPERTIES
        )

        # Enforce strict uniform aspect ratio so the pie remains perfectly circular
        ax.axis('equal')

        # Apply stylized global headers centered over the canvas
        ax.set_title(
            contribution_pie_styles.PIE_MAIN_TITLE,
            fontdict=contribution_pie_styles.TITLE_FONT_CONFIGURATION,
            loc='center',
            pad=20
        )

        # Construct legend card utilizing cleaned configuration properties
        legend = ax.legend(
            wedges,
            legend_labels,
            **contribution_pie_styles.LEGEND_PROPERTIES
        )
        legend.get_frame().set_linewidth(1)
        legend.get_frame().set_edgecolor(contribution_pie_styles.SPINE_BORDER_COLOR)

        plt.tight_layout()
        return fig
