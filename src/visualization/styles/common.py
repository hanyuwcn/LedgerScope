# =====================================================================
# MATPLOTLIB CHART DESIGN TOKENS (Keep as raw numbers)
# =====================================================================
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
# COLOR_SET = "coolwarm"
# COLOR_SET = "mako"
COLOR_SET = "viridis_r"

# Design parameters extracted cleanly out of the execution code
Y_AXIS_ROTATION = 0
Y_AXIS_PADDING = 45
TITLE_PADDING = 30

X_TICK_ROTATION = 45
Y_TICK_ROTATION = 0

# The scaling factor to bring the colorbar flush with the axis block.
CBAR_SHRINK_RATIO = 1.0

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
                       'zorder': 4}

LINE_SETTING_SMALLER = {'color': Y_AXIS_COLOR,
                        'linestyle': ':',
                        'linewidth': 2,
                        'zorder': 4}

LEGENDS_TEXT_FONTS = {'loc': 'upper left',
                      'frameon': True,
                      'facecolor': 'white',
                      'edgecolor': '#dee2e6',
                      'fontsize': 9}

# =====================================================================
# JUPYTER NOTEBOOK HTML WEB COMPONENT TOKENS (Use explicit units)
# =====================================================================
WEB_FONT_SIZE_HEADER = "0.95rem"  # Slightly larger uppercase header
WEB_FONT_SIZE_BODY = "1.0rem"  # Full baseline size for text cells
WEB_FONT_SIZE_SUB = "0.9rem"  # Muted row metadata text size
WEB_TABLE_WIDTH = "100%"

# Shared Web UI Typography and Borders
WEB_FONT_FAMILY = "'Segoe UI', Tahoma, Geneva, sans-serif"
WEB_COLOR_BORDER_LIGHT = "#dee2e6"
WEB_COLOR_BORDER_ROW = "#eee"
WEB_COLOR_HEADER_BG = "#f1f3f5"
WEB_COLOR_SUB_LABEL = "#6c757d"

COLOR_WHITE = "white"
COLOR_BLACK = "black"

# Shared Financial Grid Highlight Palettes
COLOR_HIGHLIGHT_EXP_VAL = "#4682B4"  # Heavy steel blue for expected inputs
COLOR_HIGHLIGHT_EXP_RES = "#e7f5ff"  # Light ice blue for expected outputs
COLOR_HIGHLIGHT_EXP_BORDER = "#d0ebff"

COLOR_HIGHLIGHT_THR_VAL = "#ffda6a"  # Muted gold/yellow for secondary states
COLOR_HIGHLIGHT_THR_RES = "#fff3cd"  # Light parchment yellow for secondary outputs
COLOR_HIGHLIGHT_THR_TXT = "#4d3a02"
COLOR_HIGHLIGHT_THR_RES_TXT = "#664d03"

# Shared Alert/Elasticity States
COLOR_ALERT_SUCCESS_BG = "#d4edda"
COLOR_ALERT_SUCCESS_TXT = "#155724"
COLOR_ALERT_DANGER_BG = "#f8d7da"
COLOR_ALERT_DANGER_TXT = "#721c24"


# =====================================================================
# Shared dataframe settings
# =====================================================================
def get_base_table_layout_css(header_bg, text_navy, border_light, border_row):
    """
    Generates the core structural layout and typography specifications
    for LedgerScope dashboard data tables, ensuring global UI alignment.
    """
    return [
        {
            'selector': '',
            'props': [
                ('border-collapse', 'collapse'),
                ('width', '100%'),
                ('margin', '15px 0'),
                ('border', f'1px solid {border_light}')
            ]
        },
        {
            'selector': 'th',
            'props': [
                ('background-color', header_bg),
                ('color', text_navy),
                ('padding', '12px 15px'),
                ('border-bottom', f'2px solid {border_light}'),
                ('text-align', 'right !important'),
                ('text-transform', 'uppercase'),
                ('font-size', '0.85rem')
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('padding', '10px 15px'),
                ('border-bottom', f'1px solid {border_row}'),
                ('text-align', 'right'),
                ('font-variant-numeric', 'tabular-nums')
            ]
        },
        {
            'selector': 'th.col0',
            'props': [
                ('text-align', 'right !important')
            ]
        }
    ]
