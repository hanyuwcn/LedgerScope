"""
break_even_styles.py
Dedicated design system and HTML components for Break-Even / Sensitivity tables.
"""

# High-fidelity dashboard component stylesheet isolated to break-even matrices
BREAK_EVEN_TABLE_STYLESHEET = """
<style>
    .be-dash-table { 
        border-collapse: collapse; 
        font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; 
        width: 100%; 
        margin: 15px 0; 
        border: 1px solid #dee2e6; 
    }
    .be-dash-table th { 
        background-color: #f1f3f5; 
        color: #495057; 
        padding: 12px; 
        border-bottom: 2px solid #dee2e6; 
        text-align: right; 
        text-transform: uppercase; 
        font-size: 0.85rem; 
    }
    .be-dash-table td { 
        padding: 10px 15px; 
        border-bottom: 1px solid #eee; 
        text-align: right; 
        font-variant-numeric: tabular-nums; 
    }

    .be-text-left { text-align: left !important; }
    .be-sub-label { padding-left: 25px !important; color: #6c757d; font-style: italic; font-size: 0.9rem; }

    /* Row border normalization */
    .be-output-row td { border-bottom: 2px solid #dee2e6 !important; }

    /* Data Cells Core Styling */
    .be-val-exp { background-color: #4682B4; color: white; font-weight: bold; }
    .be-res-exp { background-color: #e7f5ff; border-right: 1px solid #d0ebff; }

    /* Threshold Palette (Yellow Category) */
    .be-val-thr { background-color: #ffda6a; color: #4d3a02; font-weight: bold; }
    .be-res-thr { background-color: #fff3cd; color: #664d03; font-weight: bold; border-right: 1px solid #fff3cd; }

    /* Dynamic Darker Yellow for Unreachable Output State */
    .be-val-thr-unreachable { background-color: #d99b00; color: #261b00; font-weight: bold; border-right: 1px solid #d99b00; }
    .be-res-thr-unreachable { background-color: #fff3cd; color: #664d03; font-weight: bold; border-right: 1px solid #fff3cd; }

    /* Coordinated Feasibility Classes */
    .be-margin-safe { background-color: #2e7d32; color: #ffffff; font-weight: bold; }
    .be-margin-caution { background-color: #d4edda; color: #155724; font-weight: bold; }
    .be-margin-warning { background-color: #f8d7da; color: #721c24; font-weight: bold; }
    .be-margin-danger { background-color: #CD5C5C; color: white; font-weight: bold; }
</style>
"""

BREAK_EVEN_DASHBOARD_TEMPLATE = """
{styles}
<table class="be-dash-table">
    <thead>
        <tr>
            <th class="be-text-left">{var_header}</th>
            <th>{base_header}</th>
            <th>{thr_header}</th>
            <th>{margin_header}</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""
