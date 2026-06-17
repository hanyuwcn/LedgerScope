from matplotlib import pyplot as plt

from src.visualization.styles import histogram_distribution_styles


def plot_multiple_views(plot_functions, figsize=None):
    """
    Arranges multiple arbitrary plot functions onto a single horizontal canvas.

    Args:
        plot_functions (list): A list of callables. Each callable must
            accept a single argument 'ax' and draw on it.
        figsize (tuple, optional): Total figure size. If None, defaults to
            (width * n, height) based on histogram_distribution_styles.

    Returns:
        matplotlib.figure.Figure: The combined figure.
    """
    n = len(plot_functions)

    # Calculate responsive figsize based on your style constant
    if figsize is None:
        base_w, base_h = histogram_distribution_styles.FIGURE_SIZE
        figsize = (base_w * n, base_h)

    fig, axes = plt.subplots(1, n, figsize=figsize)

    # Ensure axes is always a list for consistent iteration
    if n == 1:
        axes = [axes]

    for ax, draw_func in zip(axes, plot_functions):
        draw_func(ax)

    fig.tight_layout()
    return fig
