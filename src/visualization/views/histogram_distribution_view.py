import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.visualization.styles import histogram_distribution_styles


def generate_histogram_from_array(simulations, output_name, goal=None, ax=None, title=None):
    """
    Generates a high-fidelity histogram showcasing data density distributions.

    This function is designed for both standalone usage and as a component
    within aggregated report layouts (e.g., via plot_multiple_views). It
    automatically detects its own context: if it creates its own axes, it
    renders as a standalone plot; if an axes is provided, it assumes an
    aggregated context and applies font scaling for readability.

    Args:
        simulations (list): A list of dictionaries containing simulation results.
        output_name (str): The key used to extract data from the simulation dicts.
        goal (float, optional): A target threshold value to draw on the plot.
            Defaults to None.
        ax (matplotlib.axes.Axes, optional): An existing axes object to draw on.
            If None, a new figure and axes are created internally.
            Defaults to None.
        title (str, optional): A custom title for the plot. If None, a
            default title is generated based on output_name. Defaults to None.

    Returns:
        matplotlib.figure.Figure: Returns the Figure object ONLY if a new one
            was created. Returns None if an 'ax' was provided.
    """
    # 1. Extract and process statistics
    data = [sim[output_name] for sim in simulations]
    data_min, data_max = min(data), max(data)
    data_mean = np.mean(data)

    colors = histogram_distribution_styles.get_threshold_boundary_colors()
    formatter = histogram_distribution_styles.get_formatter(output_name)

    # 2. Handle Canvas Creation
    created_new_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=histogram_distribution_styles.FIGURE_SIZE)
        created_new_fig = True

    # 3. Render Density Bars
    weights = np.ones_like(data) / len(data)
    _, bins, patches = ax.hist(
        data,
        weights=weights,
        **histogram_distribution_styles.HISTOGRAM_BIN_FONT
    )

    # 4. Apply Dynamic Color Gradient Fields
    norm = histogram_distribution_styles.get_gradient_normalizer(data_min, data_max)
    for bin_edge, patch in zip(bins, patches):
        patch.set_facecolor(cm.viridis_r(norm(bin_edge)))

    # 5. Draw Reference Lines
    if goal is not None:
        ax.axvline(
            x=goal,
            label=histogram_distribution_styles.HISTOGRAM_VERTICAL_LINE_GOAL.format(goal=formatter(goal)),
            **histogram_distribution_styles.LINE_SETTING_BIGGER
        )

    ax.axvline(
        x=data_mean,
        label=histogram_distribution_styles.HISTOGRAM_VERTICAL_LINE_MEAN.format(mean=formatter(data_mean)),
        **histogram_distribution_styles.LINE_SETTING_SMALLER
    )

    # 6. Overlay Comparative Performance Brackets
    if goal is not None:
        total_count = len(data)
        met_count = sum(1 for val in data if val > goal)
        pct_met = (met_count / total_count) * 100
        pct_not_met = 100.0 - pct_met

        y_max = ax.get_ylim()[1]
        y_arrow, y_text_pct = y_max * 0.92, y_max * 0.96

        ax.annotate('', xy=(data_min, y_arrow), xytext=(goal, y_arrow),
                    arrowprops=dict(arrowstyle='<->', color=colors["color_not_met"], lw=1.5))
        ax.annotate('', xy=(goal, y_arrow), xytext=(data_max, y_arrow),
                    arrowprops=dict(arrowstyle='<->', color=colors["color_met"], lw=1.5))

        ax.text((data_min + goal) / 2, y_text_pct, f"{pct_not_met:.2f}%", color=colors["color_not_met"],
                fontdict=histogram_distribution_styles.HISTOGRAM_IN_GRAPH_TEXT_FONTS)
        ax.text((data_max + goal) / 2, y_text_pct, f"{pct_met:.2f}%", color=colors["color_met"],
                fontdict=histogram_distribution_styles.HISTOGRAM_IN_GRAPH_TEXT_FONTS)

    # 7. Final Styling and Cleanup
    # If created_new_fig is True, amplify_font is False.
    # If created_new_fig is False (we were given an ax), amplify_font is True.
    histogram_distribution_styles.apply_histogram_theme(
        ax,
        output_name,
        title=title,
        amplify_font=(not created_new_fig)
    )
    sns.despine(ax=ax)

    # 8. Return the figure if we own it
    if created_new_fig:
        fig.tight_layout()
        return fig
    return None
