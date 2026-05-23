
- Have a detailed design doc after the codebase is complete

- test with same data on the old projects

- test with notebook to replicate same inputs

- review all the tests

- Add solid model pipeline so that they don't have to be constructed every single times
  - They can be composed of smaller pipeline
    - Old column concept like cost, expense. 
    - And a higher level aggregator, such as revenue, profit. 
    - And metrics, such as roi, fcf
  - they can be in a composed type like `[**cost, **revenue, **profit]` form
  - They can be created through model names creating instance as all models can have no input variables
 
- Optimize plots(Ctnd)
  - wrap up messages and variable keys
  - Add Pie chart, input could be few output results to see their percentage e.g. ["Cogs", "AdvertisingCost, Expense"]



- Write final report
 - in both languages
 - write description for every variable setting, explain what it is and where the ranges evaluation is coming from
 - Write description and formula for models
 - Use (histogram/pie chart)plot to see the variable ranges for smaller aggregate, like cost and expense. 


    - Workflow
      - go through each module with AI to discuss the interfaces and functionality 
      - discuss on the project layout and description, readme 

    - Add GUARDRAIL in the evaluate_chained_models to prevent used parameters was refreshing new values causing a conflict. 
      - This should more of a model sequence issue rather than parameter issue. 
      - Flow: Detecting a circle in a graph. input values of previous models cannot be later models' output

    - _evaluate_single_iteration shall be a public method and to be tested
    
    - slightly modify validation functions
      - make check_variables_for_function return true and add test
      - rename is_model_sequence_valid to check_model_pipeline_topology_order

    - Optimize model behaviors
      - Have a description for each model(in docstring), 
        - can be details like "Evaluating COGS from Cost of Goods Sold = PurchasingPrice * Orders * ItemsPerOrder"
      - Reconsider the approach of making optional variables a dictionary
      - depreciation, capEx can be set with optional

    - Optimize plots
        - Should only target on input variable, any variables later to be refreshed is meaningless
        - Either all green or all yellow, how can they be partially green partially yellow? 
          - Answer: purchasing price and cpa are negative factor, or sometime slices are too big  
      - methods like "_format_value", f"{elasticity_val:+.2f}", f"{num_val:,.4f}" should be written as public methods
        - with an option by adding "¥" 
        - Making a map from variable name to its conversion function