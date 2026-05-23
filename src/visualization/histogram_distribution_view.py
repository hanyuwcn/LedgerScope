import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.config import plots
from .histogram_distribution_styles import *


def generate_histogram_from_array(simulations, output_name, goal=None):
    """
    Generates a high-fidelity histogram showcasing data density distributions
    with custom gradient mapping based on your systemic analytics configuration.

    Parameters
    ----------
    simulations : list of dict
        A collection of simulation results, where each record maps metric keys
        to their numerical runtime outputs.
    output_name : str
        The specific target metric variable key to extract and map from the execution space
        (e.g., variable_names.MODEL_DEFAULT_OUTPUT_NAME). Serves as a required argument.
    goal : float or int, optional
        A target threshold value. When provided, the engine highlights progress
        via split percentage calculations, range brackets, and goal markers.
        Defaults to None.

    Returns
    -------
    matplotlib.figure.Figure
        The engineered histogram canvas styled via localized runtime overrides.
    """
    stats = compute_simulation_stats(simulations, output_name)
    colors = get_threshold_boundary_colors()

    # 1. Isolate layout changes from leaking globally
    with plt.rc_context():
        fig, ax = plt.subplots(figsize=plots.FIGURE_SIZE)

        # 2. Render Density Bars
        weights = np.ones_like(stats["data"]) / len(stats["data"])
        n, bins, patches = ax.hist(
            stats["data"],
            weights=weights,
            **plots.HISTOGRAM_BIN_FONT
        )

        # 3. Apply Theme Color Field
        norm = get_gradient_normalizer(stats["min"], stats["max"])
        for bin_edge, patch in zip(bins, patches):
            patch.set_facecolor(cm.viridis_r(norm(bin_edge)))

        # 4. Draw Threshold Evaluation Anchors
        if goal is not None:
            ax.axvline(
                x=goal,
                label=plots.HISTOGRAM_VERTICAL_LINE_GOAL.format(goal=get_formatter(output_name)(goal)),
                **plots.LINE_SETTING_BIGGER
            )

        ax.axvline(
            x=stats["mean"],
            label=plots.HISTOGRAM_VERTICAL_LINE_MEAN.format(mean=get_formatter(output_name)(stats["mean"])),
            **plots.LINE_SETTING_SMALLER
        )

        # 5. Overlay Comparative Distribution Brackets
        if goal is not None:
            pct_met, pct_not_met = compute_target_percentages(stats["data"], goal)
            y_max = ax.get_ylim()[1]
            y_arrow, y_text_pct = y_max * 0.92, y_max * 0.96

            # Dynamic structural direction brackets
            ax.annotate('', xy=(stats["min"], y_arrow), xytext=(goal, y_arrow),
                        arrowprops=dict(arrowstyle='<->', color=colors["color_not_met"], lw=1.5))
            ax.annotate('', xy=(goal, y_arrow), xytext=(stats["max"], y_arrow),
                        arrowprops=dict(arrowstyle='<->', color=colors["color_met"], lw=1.5))

            # Numerical split annotations
            ax.text((stats["min"] + goal) / 2, y_text_pct, f"{pct_not_met:.2f}%", color=colors["color_not_met"],
                    fontdict=plots.HISTOGRAM_IN_GRAPH_TEXT_FONTS)
            ax.text((stats["max"] + goal) / 2, y_text_pct, f"{pct_met:.2f}%", color=colors["color_met"],
                    fontdict=plots.HISTOGRAM_IN_GRAPH_TEXT_FONTS)

        # 6. Legends & Labeling Composition
        ax.legend(**plots.HISTOGRAM_IN_LEGENDS_TEXT_FONTS)
        ax.set_title(label=plots.HISTOGRAM_TITLE_CONTEXT.format(output=output_name), fontdict=plots.TITLE_FONT, pad=50)

        # 7. Apply Axis Transformation Transformers
        x_fmt, y_fmt = get_axis_formatters(output_name)
        ax.xaxis.set_major_formatter(x_fmt)
        ax.yaxis.set_major_formatter(y_fmt)

        # 8. Structural Layout Finalization
        ax.tick_params(axis='x', colors=plots.X_AXIS_COLOR, labelsize=plots.TICK_SIZE, labelrotation=45)
        ax.tick_params(axis='y', colors=plots.Y_AXIS_COLOR, labelsize=plots.TICK_SIZE)

        ax.set_xlabel(xlabel=plots.HISTOGRAM_X_LABEL_CONTEXT.format(output=output_name), fontdict=plots.X_AXIS_FONT)
        ax.set_ylabel(ylabel=plots.HISTOGRAM_Y_LABEL_CONTEXT, fontdict=plots.Y_AXIS_FONT, rotation=0, labelpad=60)

        sns.despine(ax=ax)
        fig.tight_layout()

        return fig
