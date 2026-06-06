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

# Shared dataframe settings
## TODO: apply this table style for break even analysis and comparative statics
SHARED_TABLE_BASE_STYLE = f"""
    .ls-dashboard-table {{
        border-collapse: collapse;
        font-family: {WEB_FONT_FAMILY};
        width: 100%;
        margin: 15px 0;
        border: 1px solid {WEB_COLOR_BORDER_LIGHT};
    }}
    .ls-dashboard-table th {{
        background-color: {WEB_COLOR_HEADER_BG};
        color: {COLOR_NAVY};
        padding: 12px 15px;
        border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT};
        text-align: right;
        text-transform: uppercase;
        font-size: 0.85rem;
    }}
    .ls-dashboard-table td {{
        padding: 10px 15px;
        border-bottom: 1px solid {WEB_COLOR_BORDER_ROW};
        text-align: right;
        font-variant-numeric: tabular-nums;
    }}
    .text-left {{ text-align: left !important; }}
    .sub-label {{ padding-left: 25px !important; color: {WEB_COLOR_SUB_LABEL}; font-style: italic; font-size: 0.9rem; }}
"""

# Optimized HTML framework reusable by any matrix view layer
## TODO: apply this table style for break even analysis and comparative statics
SHARED_DASHBOARD_HTML_TEMPLATE = """
{styles}
<table class="ls-dashboard-table">
    <thead>
        <tr>
            {headers}
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""
