# LedgerScope — Technical Design Document (Draft)

This document establishes the architecture for **LedgerScope**, a lightweight, stateless financial simulation and sensitivity analysis engine.

---

## 1. System Overview & Core Philosophy

Traditional financial modeling tools suffer from complex object-oriented inheritance traps, tight coupling, and state mutation bugs (such as "state bleed" during iterative loop sweeps).

LedgerScope solves these issues by enforcing a strict separation between **Data Definition** and **Mathematical Execution**. The engine relies on a clean Model-View-Controller (MVC) separation:

* **The Blueprint (Model/Data):** Unified, stateless variables defining names and analysis ranges.
* **The Logic (Controller):** Stateless execution models chained in an explicit, user-defined topological sequence.
* **The View (Visualization):** A decoupled module that transforms raw multi-coordinate arrays into strategic dashboards.

---

## 2. Core Components

### 2.1 The Unified `Variable` Class

Instead of dividing variables into complex "Independent" or "Dependent" subclasses, LedgerScope treats all data elements identically. A variable simply maintains an identity (name) and a numerical boundary.

The role a variable plays—whether it is an input or a calculated outcome—is determined purely by the simulation context. Variable initialization gracefully covers five distinct states based on the parameters provided:

1. **Full Window:** Min, max, and expected values are explicitly defined (highly volatile inputs).
2. **Static Constant:** Only an expected value is provided; boundaries collapse to match it (e.g., fixed corporate rent).
3. **Range Bound:** Only min and max are provided; expected value defaults to the midpoint.
4. **Bounded Floor:** Only a max value is provided; min defaults to 0.
5. **Pure Placeholder:** No values are provided (All `None`). Used for downstream calculated metrics (e.g., Net Income) that start empty and are populated by models.

### 2.2 The `GenericModel` Class

Models are purely functional, stateless transformation engines. They take a primitive dictionary of numbers, execute an aggregated calculation, and return an enriched payload.

* **Pass-Through Ledger Payload:** Inputs flow seamlessly into the model. The model appends its new calculations directly onto the incoming data dictionary and passes the entire updated ledger downstream. This ensures organic data lineage tracking.
* **Flexible Execution (`kwargs`):** Core mathematical formulas are passed as flexible Python callables using keyword arguments. This allows the logic to ingest the full payload, pull what it needs, ignore unrelated variables, and smoothly handle optional parameters via fallback defaults (e.g., currency exchange rates).
* **Defensive Guardrails:** A two-tier validation system (`check_variables`) ensures that required fields are present before heavy compute loops begin, and verifies that the mathematical function successfully generated its promised output keys.

---

## 3. Analysis Layer & Execution Flow

To avoid heavy graph-traversal algorithms and eliminate the risk of infinite cyclic dependency loops, LedgerScope offloads pipeline sequencing to configuration time.

```
[Primitive Input Dict] ──> Model 1 (e.g., Expense) ──> Enriched Ledger ──> Model 2 (e.g., Profit) ──> Final Lineage Ledger

```

1. **Topological Sequence:** The user supplies a pre-ordered list of chained models to the analysis engine.
2. **Primitive Separation:** The caller provides raw input dictionaries containing only primitive types to the sequence loop, isolating the math from any external state corruption.
3. **Coordinate Generation:** The engine sweeps across the ranges of specified variables, executing the model chain at each coordinate step to compile clean data collections.

---

## 4. Decoupled Visualization Suite

The analysis engine outputs standardized, equal-sized data collections and tabular matrices that plug directly into visualization modules:

* **Linear Regressions:** Takes matched $X/Y$ parameter lists to compute trend lines and mathematically isolate marginal returns.
* **Bivariate Heatmaps:** Cross-examines two varying primitives simultaneously to expose operational "safety zones" and "danger zones" (e.g., where profit turns negative).
* **Risk Histograms:** Clusters outputs from multi-variable randomized runs to build clear statistical probability distributions for corporate decision-making.