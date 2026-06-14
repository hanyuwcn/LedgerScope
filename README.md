# LedgerScope

**General-purpose financial modeling framework** — Quickly build business financial models supporting sensitivity analysis, Monte Carlo simulation, and visualization.

## Overview

LedgerScope is a reusable financial modeling framework providing core abstractions (Variable, Model, Pipeline, Analysis, Visualization) to help analysts quickly build financial models for scenarios including cross-border trade, e-commerce, and SaaS.

## Requirements

- **Python 3.8+**

## Core Features

- **Variable Management**: Range definition, random sampling, extreme value extraction
- **Model Pipeline**: Sequential execution of calculation modules with automatic dependency resolution
- **6 Analysis Modes**: Break-even, sensitivity analysis, Monte Carlo simulation, regression analysis, contribution analysis, two-way sensitivity analysis
- **Visualization Dashboards**: Tables, pie charts, histograms, scatter plots, heatmaps
- **Audit Mechanism**: Validate cross-model data consistency

## Quick Start

### Installation

```bash
git clone https://github.com/hanyuwcn/LedgerScope/
cd LedgerScope
pip install -r requirements.txt
```

### 5-Minute Example: Analyzing Revenue Impact on Valuation

```python
import matplotlib.pyplot as plt
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.analysis import stochastic_bivariate_simulation
from src.visualization import generate_linear_regression_from_lists

# 1. Define variables
variables = {
    "Revenue": Variable(min=80000, exp=100000, max=120000),
    "Cost": Variable(min=30000, exp=40000, max=50000),
    "PeRatio": Variable(min=5, exp=8, max=10)
}

# 2. Build model pipeline
pipeline = [NetIncomeModel(), MarketPriceModel()]

# 3. Execute regression analysis
x, y, stats = stochastic_bivariate_simulation(
    variables=variables,
    independent_target_x="Revenue",
    dependent_target_y="MarketPrice",
    shuffled_variables=["Revenue", "Cost"],
    model_pipeline=pipeline,
    sample_size=100
)

# 4. Visualize
fig = generate_linear_regression_from_lists(x, y, "Revenue", "MarketPrice")
plt.show()
```

## Documentation

- [Design Document](docs/design.md) — Complete architecture description
- [Sample Notebooks](samples/) — 6 analysis examples

## Project Structure

```
LedgerScope/
├── src/
│   ├── core/          # Base classes (Variable, Model, Auditor)
│   ├── variables/     # Independent variable definitions
│   ├── models/        # Financial model implementations
│   ├── pipelines/     # Model composer
│   ├── engine/        # Execution engine
│   ├── analysis/      # 6 analysis modes
│   ├── visualization/ # Visualization (7 views)
│   ├── auditors/      # Data consistency audit
│   ├── config/        # Configuration management
│   └── utils/         # Utility functions
├── samples/           # Jupyter Notebook examples
├── tests/             # Unit tests
└── docs/              # Design documentation
```

## Analysis Modes at a Glance

| Mode | Function | Visualization | Purpose |
|:---|:---|:---|:---|
| Break-even | `break_even_analysis` | Table | Find break-even point |
| Comparative statics | `comparative_statics` | Table + Elasticity | Calculate sensitivity |
| Contribution | `stochastic_contribution_analysis` | Pie chart | Average proportions |
| Monte Carlo | `run_monte_carlo` | Histogram | Probability distribution |
| Regression | `stochastic_bivariate_simulation` | Scatter + Regression line | Linear relationship |
| Two-way sensitivity | `run_two_way_sensitivity_analysis` | Heatmap | Interaction effects |

## Version

Current version: **1.1.0**

## Author

@hanyuwcn

## License

Apache License 2.0
