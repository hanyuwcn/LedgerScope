import matplotlib.pyplot as plt
import numpy as np

from src.config import plots
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from .contribution_pie_styles import (
    PIE_COLORMAP,
    SPINE_BORDER_COLOR,
    TITLE_FONT_CONFIGURATION,
    IN_LEGEND_TEXT_FONTS,
    CANVAS_FIGURE_SIZE,
    PIE_MAIN_TITLE,
    X_AXIS_COLOR_RULE
)


def _get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


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
    # If the simulation returns all zeros, provide equal epsilon values
    # to let matplotlib draw equal slices safely without crashing.
    if total_sum <= 0.0:
        plot_values = np.full_like(raw_values, 1e-9)
    else:
        plot_values = raw_values

    # Derive balanced discrete colors along the spectrum
    if len(labels) > 1:
        slice_colors = PIE_COLORMAP(np.linspace(0.1, 0.9, len(labels)))
    else:
        slice_colors = [PIE_COLORMAP(0.5)]

    graph_labels = []
    legend_labels = []

    for var_name, val in average_contributions.items():
        formatter = _get_formatter(var_name)
        formatted_val = formatter(val)

        # Calculate percentage safely from division by zero errors
        pct = (val / total_sum * 100.0) if total_sum > 0.0 else 0.0

        graph_labels.append(f"{var_name}\n({pct:.1f}%)")
        legend_labels.append(f"{var_name} ({formatted_val})")

    # Isolate global style contexts to eliminate downstream side-effects
    with plt.rc_context():
        fig, ax = plt.subplots(dpi=100, figsize=CANVAS_FIGURE_SIZE)

        wedges, texts = ax.pie(
            plot_values,
            labels=graph_labels,
            colors=slice_colors,
            startangle=140,
            textprops={
                'fontsize': plots.LINEAR_REGRESSION_TICK_SIZE,
                'color': X_AXIS_COLOR_RULE
            },
            wedgeprops={
                'edgecolor': SPINE_BORDER_COLOR,
                'linewidth': 1,
                'antialiased': True
            }
        )

        # Enforce strict uniform aspect ratio so the pie remains perfectly circular
        ax.axis('equal')

        # Apply stylized global headers centered over the canvas
        ax.set_title(
            PIE_MAIN_TITLE,
            fontdict=TITLE_FONT_CONFIGURATION,
            loc='center',
            pad=20
        )

        # Construct legend card containing explicit names and formatted absolute values
        legend = ax.legend(
            wedges,
            legend_labels,
            title="Components",
            **IN_LEGEND_TEXT_FONTS
        )
        legend.get_frame().set_linewidth(1)
        legend.get_frame().set_edgecolor(SPINE_BORDER_COLOR)

        plt.tight_layout()

        return fig
