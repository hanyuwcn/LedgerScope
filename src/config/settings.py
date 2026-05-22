# src/ledgerscope/config/settings.py

# =====================================================================
# SYSTEM ENVIRONMENT VARIABLES
# =====================================================================
NUMS_IN_RANGE = 50  # Granularity/steps for variable sweeps and heatmaps
DECIMAL_ROUNDING = 4  # Precision cap for floating-point calculations
SAMPLE_SIZE = 100  # Total iterations for randomized Monte Carlo runs

# =====================================================================
# FINANCIAL PARAMETER DEFAULTS
# =====================================================================
### Default Constants (For Fallbacks in Functions)
COST_DEFAULT_CPA = 30
COST_DEFAULT_CONVERSION_RATE = 0.1
DEFAULT_CURRENCY_RATE = 6.8
TAX_RATE = 0.2

### Boundary Defaults (For Rule 1 / Variable Initialization Ranges)
USD_TO_RMB_LOWER = 6.4
USD_TO_RMB_UPPER = 7.0

INTEREST_RATE_LOWER = 0.01
INTEREST_RATE_UPPER = 0.03

CPA_LOWER = 12
CPA_UPPER = 36
