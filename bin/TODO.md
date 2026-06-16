- Review all the tests

- Write final report(ctnd)
   - Restructure final report
   - Write report in both languages
   - Pie chart for price waterfall analysis

- Have a detailed design doc after codebase completion
   - Write Design doc in both languages


    - Workflow
      - go through each module with AI to discuss the interfaces and functionality 
      - discuss on the project layout and description, readme 


    - Analysis
      - _evaluate_single_iteration shall be a public method and to be tested
      - Add GUARDRAIL in the evaluate_chained_models to prevent used parameters was refreshing new values causing a conflict. 
        - This should more of a model sequence issue rather than parameter issue. 
        - Flow: Detecting a circle in a graph. input values of previous models cannot be later models' output
      - breakdown_metrics in pie-chart need to be verified.
    
    - slightly modify validation functions
      - make check_variables_for_function return true and add test
      - rename is_model_sequence_valid to check_model_pipeline_topology_order


      - Optimize plots
        - Should only target on input variable, any variables later to be refreshed is meaningless
        - Either all green or all yellow, how can they be partially green partially yellow? 
          - Answer: purchasing price and cpa are negative factor, or sometime slices are too big  
        - methods like "_format_value", f"{elasticity_val:+.2f}", f"{num_val:,.4f}" should be written as public methods
          - with an option by adding "¥" 
          - Making a map from variable name to its conversion function
        - Add Pie chart, input could be few output results to see their percentage e.g. ["Cogs", "AdvertisingCost, Expense"]
        - wrap up messages and variable keys
        - Resolve to-dos in the views and styles in plots
        - Replace html with dataframe plot
        - categorize styles and views so that they don't have to be with each other.
        - move plots from config to style as common-style. by following steps
          1. Distributes all attributes to each style;
          2. Collect common styles together
          3. Organize by order
        - Figure out proper time to plot.close()
        - Fix linear regression number check: if np.var(x_values) == 0.0 or np.var(y_values) == 0.0 by math.isclose()

      - Add solid model pipeline so that they don't have to be constructed every single times
        - They can be composed of smaller pipeline
          - Old column concept like cost, expense. 
          - And a higher level aggregator, such as revenue, profit. 
          - And metrics, such as roi, fcf
        - they can be in a composed type like `[**cost, **revenue, **profit]` form
        - They can be created through model names creating instance as all models can have no input variables

      - Implement google search ads efficiency model
        - Together with roas and cpl model

      - categorize models into sub folders.
        - make parent folder import all models. This makes the outer scope unaware of structural folders

      - Write final report
        - in both languages
        - write description for every variable setting, explain what it is and where the ranges evaluation is coming from
        - Write description and formula for models
        - Use (histogram/pie chart)plot to see the variable ranges for smaller aggregate, like cost and expense. 

      - Optimize models
        - Have a description for each model(in docstring), 
          - can be details like "Evaluating COGS from Cost of Goods Sold = PurchasingPrice * Orders * ItemsPerOrder"
        - Reconsider the approach of making optional variables a dictionary
        - depreciation, capEx can be set with optional
        - 0 denominator protections for CPL, CAC, UnitContributionMargin, ROI, roas
        - Optimize models with optional_variable_getter and required_variable_getter
        - remove get_name() methods from base_model
        - Modify variables to min, exp, max
        - Remove prefix for each variable names
        - Setup cost
        - Deduction rate
        - Deprecate advertising_efficiency_model, as more detailed ads models are implemented
        - Deprecate purchasing price and selling price
        - ExwModel(for simplicity reason, shipping cost will be counted as % in deduction cost)
        - MarketPrice = Price-to-ratio * 12 * net income / months
        - Correct analysis tests and visualization tests
        - Replace `variable_names.` to `vn`
        - separate freight for seller freight and buyer freight. auditor for only one of them > 0
