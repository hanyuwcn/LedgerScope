import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.visualization.styles import histogram_distribution_styles


def generate_histogram_from_array(simulations, output_name, goal=None):
    """
    Generates a high-fidelity histogram showcasing data density distributions
    with custom gradient mapping based on your systemic analytics configuration.
    """
    # 1. Extract simulation statistics locally in the view engine layer
    data = [sim[output_name] for sim in simulations]
    data_min, data_max = min(data), max(data)
    data_mean = np.mean(data)

    colors = histogram_distribution_styles.get_threshold_boundary_colors()
    formatter = histogram_distribution_styles.get_formatter(output_name)

    # 2. Isolate layout changes from leaking globally
    with plt.rc_context():
        fig, ax = plt.subplots(figsize=histogram_distribution_styles.FIGURE_SIZE)

        # 3. Render Density Bars
        weights = np.ones_like(data) / len(data)
        n, bins, patches = ax.hist(
            data,
            weights=weights,
            **histogram_distribution_styles.HISTOGRAM_BIN_FONT
        )

        # 4. Apply Dynamic Color Gradient Fields
        norm = histogram_distribution_styles.get_gradient_normalizer(data_min, data_max)
        for bin_edge, patch in zip(bins, patches):
            patch.set_facecolor(cm.viridis_r(norm(bin_edge)))

        # 5. Draw Threshold and Mean Reference Lines
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

            # Render bracket annotations
            ax.annotate('', xy=(data_min, y_arrow), xytext=(goal, y_arrow),
                        arrowprops=dict(arrowstyle='<->', color=colors["color_not_met"], lw=1.5))
            ax.annotate('', xy=(goal, y_arrow), xytext=(data_max, y_arrow),
                        arrowprops=dict(arrowstyle='<->', color=colors["color_met"], lw=1.5))

            # Numerical text placements
            ax.text((data_min + goal) / 2, y_text_pct, f"{pct_not_met:.2f}%", color=colors["color_not_met"],
                    fontdict=histogram_distribution_styles.HISTOGRAM_IN_GRAPH_TEXT_FONTS)
            ax.text((data_max + goal) / 2, y_text_pct, f"{pct_met:.2f}%", color=colors["color_met"],
                    fontdict=histogram_distribution_styles.HISTOGRAM_IN_GRAPH_TEXT_FONTS)

        # 7. Apply the Unified Presentation Theme
        histogram_distribution_styles.apply_histogram_theme(ax, output_name)

        # 8. Structural Layout Cleanup
        sns.despine(ax=ax)
        fig.tight_layout()
        # plt.close()
        return fig
