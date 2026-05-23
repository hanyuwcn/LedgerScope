"""
CSS Layout Configuration for Comparative Statics Dashboard.
Following the project's isolated view styling pattern.
"""

COMPARATIVE_STATICS_STYLE = """
<style>
    .cs-table { border-collapse: collapse; font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; width: 100%; margin: 15px 0; border: 1px solid #dee2e6; }
    .cs-table th { background-color: #f1f3f5; color: #495057; padding: 12px 15px; border-bottom: 2px solid #dee2e6; text-align: right; text-transform: uppercase; font-size: 0.85rem; }
    .cs-table td { padding: 10px 15px; border-bottom: 1px solid #eee; text-align: right; font-variant-numeric: tabular-nums; }

    .text-left { text-align: left !important; }
    .sub-label { padding-left: 25px !important; color: #6c757d; font-style: italic; font-size: 0.9rem; }

    /* Row Base Overrides */
    .row-factor { background-color: #f8f9fa; }
    .row-output { background-color: #ffffff; }

    /* Color Configurations */
    .val-heavy-blue { background-color: #4682B4; color: white; font-weight: bold; }
    .res-light-blue { background-color: #e7f5ff; border-right: 1px solid #d0ebff; font-weight: bold; }

    .val-light-yellow { background-color: #ffda6a; color: #4d3a02; font-weight: bold; }
    .res-dark-yellow { background-color: #fff3cd; color: #664d03; font-weight: bold; border-right: 1px solid #fff3cd; }

    .elasticity-positive { background-color: #d4edda; color: #155724; font-weight: bold; }
    .elasticity-negative { background-color: #f8d7da; color: #721c24; font-weight: bold; }
</style>
"""
