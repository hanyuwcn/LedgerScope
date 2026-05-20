from statistics import mean

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from matplotlib import cm

from src.config import variable_names, plots


def generate_histogram_from_array(simulations, goal, output_name=variable_names.MODEL_DEFAULT_OUTPUT_NAME):
    fig, ax = plt.subplots(figsize=plots.FIGURE_SIZE)

    # 1. Stats
    data = [simulation[output_name] for simulation in simulations]
    data_min, data_max = min(data), max(data)
    data_mean = mean(data)
    percentage_met = get_percentage_surpass(data, goal) * 100
    percentage_not_met = 100 - percentage_met

    # 2. Plot Histogram Bars
    n, bins, patches = ax.hist(data, **plots.HISTOGRAM_BIN_FONT)

    # 3. Apply Gradient of colors
    norm = plt.Normalize(data_min, data_max)
    for bin_edge, patch in zip(bins, patches):
        patch.set_facecolor(cm.coolwarm(norm(bin_edge)))

    # 4. Vertical Lines with Labels for the Legend
    # We add labels here so plt.legend() can find them
    ax.axvline(x=goal, label=plots.HISTOGRAM_VERTICAL_LINE_GOAL.format(goal=goal),
               **plots.LINE_SETTING_BIGGER)

    ax.axvline(x=data_mean, label=plots.HISTOGRAM_VERTICAL_LINE_MEAN.format(mean=data_mean),
               **plots.LINE_SETTING_SMALLER)

    # 6. Arrows & Percentages (Cleaned up top area)
    y_max = ax.get_ylim()[1]
    y_arrow, y_text_pct = y_max * 0.92, y_max * 0.96

    ax.annotate('', xy=(data_min, y_arrow), xytext=(goal, y_arrow),
                arrowprops=dict(arrowstyle='<->', color=plots.COLOR_BLUE, lw=1.5))
    ax.annotate('', xy=(goal, y_arrow), xytext=(data_max, y_arrow),
                arrowprops=dict(arrowstyle='<->', color=plots.COLOR_RED, lw=1.5))

    ax.text((data_min + goal) / 2, y_text_pct, f"{percentage_not_met:.2f}%", color=plots.COLOR_BLUE,
            fontdict=plots.HISTOGRAM_IN_GRAPH_TEXT_FONTS)
    ax.text((data_max + goal) / 2, y_text_pct, f"{percentage_met:.2f}%", color=plots.COLOR_RED,
            fontdict=plots.HISTOGRAM_IN_GRAPH_TEXT_FONTS)

    # 7. THE LEGEND (Replacing the "awkward" top tag)
    ax.legend(**plots.HISTOGRAM_IN_LEGENDS_TEXT_FONTS)

    # 8. Final Styling
    ax.set_title(label=plots.HISTOGRAM_TITLE_CONTEXT.format(output=output_name), fontdict=plots.TITLE_FONT, pad=50)

    ax.tick_params(axis='x', colors=plots.X_AXIS_COLOR, labelsize=plots.TICK_SIZE, labelrotation=45)
    ax.tick_params(axis='y', colors=plots.Y_AXIS_COLOR, labelsize=plots.TICK_SIZE)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))

    ax.set_xlabel(xlabel=plots.HISTOGRAM_X_LABEL_CONTEXT.format(output=output_name), fontdict=plots.X_AXIS_FONT)
    ax.set_ylabel(ylabel=plots.HISTOGRAM_Y_LABEL_CONTEXT, fontdict=plots.Y_AXIS_FONT, rotation=0, labelpad=60)

    sns.despine(ax=ax)  ## Optional, commenting to add right and top edge.

    fig.tight_layout()

    # plt.show()
    return fig


def get_percentage_surpass(data, goal):
    return sum(1 for x in data if x > goal) / len(data)
