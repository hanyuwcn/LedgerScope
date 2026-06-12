# =====================================================================
# SYSTEM ENVIRONMENT VARIABLES
# =====================================================================
NUMS_IN_RANGE = 50  # Granularity/steps for variable sweeps and heatmaps
DECIMAL_ROUNDING = 4  # Precision cap for floating-point calculations
SAMPLE_SIZE = 5000  # Total iterations for randomized Monte Carlo runs
ABS_TOL = 1e-12

# =====================================================================
# Audit & Reconciliation Settings
# =====================================================================
AUDIT_REL_TOL = 1e-3  # Relative tolerance for financial reconciliation
AUDIT_ABS_TOL = 1e-2  # Absolute tolerance for small-value reconciliation

# =====================================================================
# Default Constants (For Fallbacks in Functions)
# =====================================================================
DEFAULT_CURRENCY_RATE = 6.8
DEFAULT_TAX_RATE = 0.2
DEFAULT_TARIFF_RATE = 0.25
DEFAULT_PE_RATIO = 8
