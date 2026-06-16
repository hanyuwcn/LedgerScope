
---

## [1.2.0] - 2026-06-16

### Added

#### Core Framework Auditors

* Added `UnitGrossProfitAuditor` — Validates `UnitGrossProfit = UnitFOBPrice - UnitEXWPrice`
* Added `UnitOperatingIncomeAuditor` — Validates `UnitOperatingIncome` waterfall (FOB - EXW - Marketing - FixedOverhead) while enforcing `UnitFreightExpense = 0` as a business rule
* Added `DeductionAuditor` — Validates deduction rate bounds (`0 < Rate < 1`) and reconciles the USD-denominated pricing waterfall

#### Refactored Models

* `NetIncomeModel` — Refactored to derive after-tax profitability directly from `OperatingIncome`
* `TotalExpenseModel` — Refactored to treat `ManagementExpense` and `SellingExpense` as optional inputs (defaulting to 0.0)
* `AdvertisingExpenseModel` — Added model for 1:1 marketing-to-advertising budget allocation

### Changed

#### Model Architecture Refinement

* **Parameter Flexibility:** Migrated several models (e.g., `TotalExpenseModel`) from mandatory required inputs to optional inputs, providing greater resilience for partial financial datasets.
* **Business Logic Enforcement:** Integrated "Forced Zero" logic into the `UnitOperatingIncomeAuditor` to ensure freight costs are correctly excluded from Brand-side profitability calculations regardless of raw input values.
* **Standardized Docstrings:** Updated all models and auditors with consistent reconciliation formulas, logic descriptions, and input/output mappings to match the `1.1.0` architectural standards.

#### Test Suite Updates

* **Engine Runner:** Updated `runner.py` test suite to reflect the new pipeline structure and updated mathematical traces (Units -> COGS -> Advertising -> Selling -> Total Expense).
* **Validation:** Added full unit test coverage for the three new auditors and refactored models, ensuring circuit breakers trigger correctly on reconciliation failures.

### Design Benefits

| Benefit | Description |
| --- | --- |
| **Pipeline Reliability** | New auditor suite ensures the Price Waterfall remains internally consistent during multi-stage execution |
| **Business Rule Compliance** | Centralized freight exclusion logic in the auditor prevents "leaky" cost accounting |
| **Input Robustness** | Optionality in cost models allows for lean execution paths without requiring dummy zero-value inputs |
| **Auditability** | Formulas and logic are now explicitly documented in class docstrings, facilitating easier peer review |

### Migration Guide (Upgrading from 1.1.0 to 1.2.0)

**For model initialization:**

* Optional variables now rely on default dictionary fallbacks. Ensure that new model instances do not require empty keys for `MANAGEMENT_EXPENSE` or `SELLING_EXPENSE` in the input dictionary.

**For pipeline integration:**

* Integrate the new `UnitGrossProfitAuditor`, `UnitOperatingIncomeAuditor`, and `DeductionAuditor` into the `PipelineComposer` to ensure the integrity of the updated Price Waterfall calculation.

---

## [1.1.0] - 2026-06-13

### Changed

#### Core Framework Refactoring: Data Retrieval Responsibility Moved to Base Classes

**Model Base Class**
- Added `_get_variable_value(name, is_optional)` private method to encapsulate variable resolution logic
- Added `prepare_calculation_context()` method to uniformly merge required and optional variables into a single dictionary
- Simplified `update_input_variable()` logic, removed compatibility with `get_name()` / `get_value()` interfaces
- `evaluate()` flow changes:
  - Old: `check_variables()` → `_model_function(optional_variables, **kwargs)` → merge results
  - New: `check_variables()` → `prepare_calculation_context()` → `_model_function(context)` → merge results

**Auditor Base Class**
- Inherits `prepare_calculation_context()` method from Model base class
- `evaluate()` flow changes:
  - Old: `check_variables()` → `_model_function(optional_variables, **kwargs)` → return original state
  - New: `check_variables()` → `super().prepare_calculation_context()` → `_model_function(context)` → return original state
- `output_names` property remains returning empty list (auditors produce no new variables)

**Calculation/Validation Function Signature Changes**

| Component | 1.0.0 Signature | 1.1.0 Signature |
|:---|:---|:---|
| Model calculation function | `def func(optional_variables: dict, **kwargs) -> dict` | `def func(variables: dict) -> dict` |
| Auditor validation function | `def check(optional_variables: dict, **kwargs) -> None` | `def check(variables: dict) -> None` |

**Affected Models (22 total, all updated)**

All model calculation functions have been refactored to the new signature, removing internal `kwargs.get(key, default)` boilerplate:

- Advertising funnel (2)
- Cost modules (3)
- Deal modules (4)
- Expense modules (2)
- Revenue & Profit (4)
- Financial metrics (5)
- Placeholder models (2)

**Affected Auditors (1)**

- `PriceArchitectureAuditor` validation function refactored to new signature

### Removed

- Support for `get_name()` / `get_value()` interfaces in `Model.update_input_variable()` (unified to `name` + `expected_value` pattern)

### Design Benefits

| Benefit | Description |
|:---|:---|
| **Eliminate boilerplate** | Calculation/validation functions no longer need to write repetitive `kwargs.get(key, default)` logic |
| **Single responsibility** | Base class handles data retrieval; subclasses handle business calculation/validation |
| **Easier testing** | Calculation/validation functions depend on a single dictionary parameter, enabling independent unit testing |
| **Cleaner interface** | Function signature simplified from 2 parameters to 1 |

### Migration Guide (Upgrading from 1.0.0 to 1.1.0)

**For custom Model subclasses:**

1. Update calculation function signature:
   ```python
   # 1.0.0
   def calculate_xxx(optional_variables: dict, **kwargs) -> dict:
       value = kwargs.get(key, optional_variables[key])
   
   # 1.1.0
   def calculate_xxx(variables: dict) -> dict:
       value = variables[key]
   ```
   
---

## [1.0.0] - 2026-06-12

### Added

#### Core Framework
- Added `Variable` base class supporting min/exp/max boundaries and random sampling
- Added `Model` base class supporting required/optional variable validation and chained execution
- Added `Auditor` base class (Model specialization) for validating cross-model data consistency
- Added variable registry (`variables/`) containing 20+ business variable definitions

#### Model Library (22 models)

**Advertising Funnel**
- `AdvertisingEfficiencyGoogleSearchModel` — Ad budget → Leads
- `CostPerLeadGoogleSearchModel` — Cost per lead calculation

**Cost Modules**
- `CostOfGoodsSoldModel` — COGS calculation
- `ShippingCostModel` — Shipping cost calculation (percentage of retail price)
- `TotalCostModel` — Total operating cost aggregation (excluding setup cost)

**Deal Modules**
- `DeductionRateModel` — Deduction rate aggregation (shipping + tariff + channel markup)
- `OrderModel` — Leads → Orders conversion
- `UnitFobModel` — Retail price → FOB price (reverse pricing waterfall)
- `UnitContributionMarginModel` — Unit contribution margin

**Expense Modules**
- `MonthlyExpenseModel` — Monthly expense aggregation
- `TotalExpenseModel` — Period expense expansion

**Revenue & Profit**
- `RevenueModel` — Revenue calculation (based on FOB price)
- `ProfitModel` — Operating profit
- `NetIncomeModel` — After-tax net income
- `FreeCashFlowModel` — Free cash flow

**Financial Metrics**
- `CacModel` — Customer acquisition cost
- `RoasModel` — Return on advertising spend
- `RoiModel` — Return on investment (based on setup cost)
- `MarketPriceModel` — Company valuation (P/E multiple method)
- `PriceArchitectureModel` — Price decomposition (per-unit level)

**Placeholder Models**
- `CapitalExpenditureModel` — Capital expenditure (currently returns 0)
- `DepreciationModel` — Depreciation (currently returns 0)

#### Auditors
- `PriceArchitectureAuditor` — Validates retail price = COGS + shipping + tariff + channel margin + net profit

#### Analysis Modules (6)
- `break_even_analysis` — Multi-variable break-even analysis
- `comparative_statics` — Three-point sensitivity analysis and elasticity calculation
- `stochastic_contribution_analysis` — Monte Carlo contribution analysis
- `run_monte_carlo` — Monte Carlo simulation
- `stochastic_bivariate_simulation` — Bivariate regression analysis
- `run_two_way_sensitivity_analysis` — Two-variable grid sensitivity analysis

#### Visualization (7 views)
- `break_even_view` — Break-even results table
- `comparative_statics_view` — Sensitivity analysis table
- `contribution_pie_view` — Contribution pie chart
- `histogram_distribution_view` — Monte Carlo histogram
- `linear_regression_view` — Regression scatter plot + trend line
- `two_way_sensitivity_heatmap_view` — Heatmap

#### Pipeline & Execution Engine
- `PipelineComposer` — Scenario-based pipeline construction (supports predefined scenarios, dynamic appending, scenario merging)
- `runner.py` — 4 execution modes (chained execution, baseline scenario, random iteration, variable sweep)
- Topological order validation — Prevents variable overwrite conflicts (DAG property)

#### Configuration System
- `settings.py` — System parameters (sampling steps, precision, audit tolerances, default constants)
- `variable_names.py` — 50+ variable name constants
- `messages.py` — Log and error message templates
- `pipelines.py` — Predefined scenario configurations
- `formatting.py` — Variable formatting mappings (currency, percentage, decimal places)

#### Utility Functions
- `validation.py` — Variable missing detection, pipeline topology validation
- `formatting.py` — Numeric formatting (`fmt`)
- `logger.py` — Colored console logging + optional file output

### Changed

#### Design Adjustments
- `TotalCostModel` removed `SetupCost`, now aggregates only operating costs (COGS + ads + shipping)
- `SetupCost` repositioned as investment item, used as ROI denominator
- Unified `_model_function` signature to `(optional_variables, **kwargs)`

#### Naming Conventions
- Variable constants use `SCREAMING_SNAKE_CASE`
- Dictionary keys use PascalCase (e.g., `"Revenue"`, `"Cost"`)

### Fixed

- `monthly_expense` mapping error → corrected to `MonthlyExpenseModel`
- `total_expense` mapping correct → `TotalExpenseModel`
- `unit_fob` model missing registration → added
- `price_architecture` model missing registration → added
- `FreeCashFlowModel` double fallback → simplified to single layer
- `contribution_analysis` missing metric validation → added
- `regression_analysis` zero variance check → replaced with tolerance
- `two_way_sensitivity` outdated comments → removed

### Known Limitations (Current Version Constraints)

- Single-product model only
- Order delivery time lag ignored
- Repeat purchase and customer lifetime value ignored
- Conversion rates assumed constant
- Depreciation and CapEx are placeholders (return 0)
- Ad channel attribution assumes 100% contribution

### Future Roadmap

- Upgrade package module (upgrade_cost, upgrade_price, upgrade_rate)
- Multi-channel attribution (distinguish ad channel contributions)
- Volume discounts (non-linear COGS)
- Negative profit tax treatment (tax shield)
- Multi-product support (product_id dimension)
- Order delivery time lag
- Repeat purchase and LTV