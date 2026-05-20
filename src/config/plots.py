##Plots
ROUNDING_FORMAT = ".2f"
TICK_SIZE = 12
LABEL_SIZE = 16
TITLE_SIZE = 25
COLOR_NAVY = "#2c3e50"
# COLOR_NAVY = '#495057'
COLOR_GREY = "#808285"
COLOR_DARK = "#101820"

COLOR_BLUE = "#89a5fb"
COLOR_RED = "#f28669"

FIGURE_SIZE = (15, 8)
TITLE_COLOR = COLOR_NAVY
X_AXIS_COLOR = COLOR_DARK
Y_AXIS_COLOR = COLOR_GREY
COLOR_SET = "coolwarm"

TITLE_FONT = {'family': 'serif',
              'color': TITLE_COLOR,
              'weight': 'bold',
              # 'size': TITLE_SIZE
              'size': 14
              }

X_AXIS_FONT = {
    'family': 'sans-serif',
    'color': X_AXIS_COLOR,
    'weight': 'normal',
    'size': LABEL_SIZE
    # 'size': 10
}
Y_AXIS_FONT = {
    'family': 'sans-serif',
    'color': Y_AXIS_COLOR,
    'weight': 'normal',
    'size': LABEL_SIZE
    # 'size': 10
}

LINE_SETTING_BIGGER = {'color': X_AXIS_COLOR,
                       'linestyle': '-.',
                       'linewidth': 2,
                       'zorder': 5}

LINE_SETTING_SMALLER = {'color': Y_AXIS_COLOR,
                        'linestyle': ':',
                        'linewidth': 2,
                        'zorder': 3}

### Heatmap
HEATMAP_CONTEXT = "notebook"
HEATMAP_COLORS = COLOR_SET
HEATMAP_TITLE = "Heatmap of impact of {factor_1} & {factor_2} on {output}"

### Histogram
HISTOGRAM_TITLE_CONTEXT = "Distribution of Simulated Density Gradient of {output}"
HISTOGRAM_X_LABEL_CONTEXT = "Simulated Values of {output}"
HISTOGRAM_Y_LABEL_CONTEXT = "Frequency(%)"
HISTOGRAM_VERTICAL_LINE_GOAL = "Benchmark Goal: {goal:,.0f}"
HISTOGRAM_VERTICAL_LINE_MEAN = 'Simulations Mean: {mean:,.0f}'
HISTOGRAM_BIN_FONT = {'bins': 40,
                      'alpha': 0.8,
                      'edgecolor': 'white',
                      'linewidth': 0.5}
HISTOGRAM_IN_GRAPH_TEXT_FONTS = {'ha': 'center', 'weight': 'bold', 'family': 'serif'}
HISTOGRAM_IN_LEGENDS_TEXT_FONTS = {'loc': 'upper left',
                                   'bbox_to_anchor': (0.02, 0.88),
                                   'prop': {'family': 'serif', 'size': 10},
                                   'frameon': True,
                                   'facecolor': 'white',
                                   'edgecolor': COLOR_DARK}

## Dashboard
SENSITIVITY_VARIABLE = "Sensitivity Variable"

### Comparative statics analysis
COMPARATIVE_STATICS_COLUMN_NAME_MIN = 'Min State'
COMPARATIVE_STATICS_COLUMN_NAME_BASE = 'Base (Expected)'
COMPARATIVE_STATICS_COLUMN_NAME_MAX = 'Max State'
COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY = "Elasticity"

### Break even analysis
BREAK_EVEN_COLUMN_NAME_BASE = 'Base (Expected)'
BREAK_EVEN_COLUMN_NAME_THRESHOLD = 'BE (Threshold)'
BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN = 'Safety Margin %'

## Linear regression plot
### Linear plot is a bit different from the plots above, it applies its own style settings
LINEAR_REGRESSION_FIGURE_SIZE = (9, 5.5)
LINEAR_REGRESSION_X_AXIS_FONT = {
    'family': 'sans-serif',
    'color': X_AXIS_COLOR,
    'fontweight': 'bold',
    'size': 10
}
LINEAR_REGRESSION_Y_AXIS_FONT = {
    'family': 'sans-serif',
    'color': Y_AXIS_COLOR,
    'fontweight': 'bold',
    'size': 10
}
# LINEAR_REGRESSION_COLORS = COLOR_SET
LINEAR_REGRESSION_LINE_FORMAT = {'color': COLOR_NAVY, 'linewidth': 1.5, 'zorder': 2}
LINEAR_REGRESSION_POINT_STYLE = {'cmap': COLOR_SET,
                                 'edgecolor': 'none',
                                 'alpha': 0.9,
                                 # 'label': 'Actual Data',
                                 'zorder': 4}
LINEAR_REGRESSION_POINT_SIZE_MIN = 15
LINEAR_REGRESSION_POINT_SIZE_MAX = 80
LINEAR_REGRESSION_TITLE = "Linear Regression Analysis: {y_label} vs {x_label}"
LINEAR_REGRESSION_IN_LEGENDS_TEXT_FONTS = {'loc': 'upper left',
                                           'frameon': True,
                                           'facecolor': 'white',
                                           'edgecolor': '#dee2e6',
                                           'fontsize': 9}
LINEAR_REGRESSION_LINE_GOAL = "{label} Benchmark ({benchmark:,.2f})"
LINEAR_REGRESSION_TICK_SIZE = 9
