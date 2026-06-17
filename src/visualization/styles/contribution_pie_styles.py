from matplotlib import cm

from . import common_styles

# Color Palette Mapping Strategy
PIE_COLORMAP = cm.viridis_r
SPINE_BORDER_COLOR = '#dee2e6'

# Font Sizing and Element Configuration Rules Mapping
TITLE_FONT_CONFIGURATION = common_styles.TITLE_FONT
IN_LEGEND_TEXT_FONTS = common_styles.LEGENDS_TEXT_FONTS
CANVAS_FIGURE_SIZE = (9, 5.5)

# Typography Labels and Color Rules
PIE_MAIN_TITLE = "Stochastic Contribution Analysis Breakdowns"
X_AXIS_COLOR_RULE = common_styles.X_AXIS_COLOR
TICK_SIZE = 9

PIE_START_ANGLE = 140

# Gather standard text property settings for slice labels
SLICE_TEXT_PROPERTIES = {
    'fontsize': TICK_SIZE,
    'color': X_AXIS_COLOR_RULE
}

# Structural design attributes for individual slices
WEDGE_PROPERTIES = {
    'edgecolor': SPINE_BORDER_COLOR,
    'linewidth': 1,
    'antialiased': True
}

# Dynamic unpack kwargs dictionary for the legend card component
LEGEND_PROPERTIES = {
    'title': "Components",
    **IN_LEGEND_TEXT_FONTS
}


def scale_font(font_dict, factor):
    new_dict = font_dict.copy()
    if 'size' in new_dict:
        new_dict['size'] *= factor
    elif 'fontsize' in new_dict:
        new_dict['fontsize'] *= factor
    return new_dict
