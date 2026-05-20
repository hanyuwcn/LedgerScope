import matplotlib.pyplot as plt
import seaborn as sns

from src.config import variable_names, plots


def generate_heatmap_from_df(df, output_name=variable_names.MODEL_DEFAULT_OUTPUT_NAME):
    # 1. Global theme settings
    sns.set_theme()
    sns.set_context(plots.HEATMAP_CONTEXT)

    # 2. THE CANVAS METHOD: Create Figure and Axes first
    fig, ax = plt.subplots(figsize=plots.FIGURE_SIZE)

    # 3. Create the heatmap inside the specific 'ax'
    sns.heatmap(
        df,
        annot=False,
        fmt=plots.ROUNDING_FORMAT,
        cmap=plots.HEATMAP_COLORS,
        ax=ax  # This tells Seaborn to draw inside our pre-defined frame
    )

    # 4. Operate on the 'ax' object directly
    # Set tick labels and rotation
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Set Labels using the ax.set_ naming convention
    ax.set_xlabel(
        df.columns.name or "Factor 1",
        fontdict=plots.X_AXIS_FONT
    )
    ax.set_ylabel(
        df.index.name or "Factor 2",
        rotation=0,
        labelpad=45,
        fontdict=plots.Y_AXIS_FONT
    )
    ax.set_title(
        plots.HEATMAP_TITLE.format(factor_1=df.columns.name, factor_2=df.index.name, output=output_name),
        fontdict=plots.TITLE_FONT,
        pad=30
    )

    # 5. Tick Parameters remain functionally identical on the 'ax'
    ax.tick_params(axis='x', colors=plots.X_AXIS_COLOR, labelsize=plots.TICK_SIZE, labelrotation=45)
    ax.tick_params(axis='y', colors=plots.Y_AXIS_COLOR, labelsize=plots.TICK_SIZE)

    # 6. Layout adjustments using the 'fig' or 'plt'
    # plt.subplots_adjust(left=0.25, bottom=0.20, right=0.95, top=0.85)
    fig.tight_layout()

    # If you wanted to save the file (Financial/Academic reports often do)
    # fig.savefig("heatmap_output.png", dpi=300, bbox_inches='tight')
    # plt.show()

    return fig
