"""
break_even_heatmap_styles.py
Centralized style templates and rendering definitions for Break-Even Heatmaps.
"""
from src.config import plots

# Clean dictionary configuration for mapping explicit title and label metadata properties
HEATMAP_LABEL_PROPERTIES = {
    # "x_label_fallback": "Factor 1",
    # "y_label_fallback": "Factor 2",
    "y_axis_rotation": plots.Y_AXIS_ROTATION,
    "y_axis_padding": plots.Y_AXIS_PADDING,
    "x_tick_rotation": plots.X_TICK_ROTATION,
    "y_tick_rotation": plots.Y_TICK_ROTATION,
    "title_padding": plots.TITLE_PADDING
}
