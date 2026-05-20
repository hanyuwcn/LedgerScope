- go through each module with AI to discuss the interfaces and functionality 
- discuss on the project layout and description, readme 
- Have a general design doc 
- Implement each parts with test cases 
- Have a detailed design doc
- optional variables can be a dict with default values
- Modifying default value for tax_rate does not break tests
- Add a AdvertisingCost model. in the opposite direction as AdvertisingEfficiency

- Have a description for each model, can be details like Evaluating COGS from purchasing price, orders and items
  - Reconsider the approach of making optional variables a dictionary
  - depreciation, capEx can be set with optional

- test with same data on the old projects

- test with notebook to replicate same inputs

- review all the tests

- wrap up messages and variable keys

- heap map should round axis number to 2 digits, also avoid value range being set with 1e6
- break even data is inconsistent
  - also check use the threshold mark to highlight colors
- histograms x axis uses .3n style

    - Add GUARDRAIL in the evaluate_chained_models to prevent used parameters was refreshing new values causing a conflict. 
      - This should more of a model sequence issue rather than parameter issue. 
      - Flow: Detecting a circle in a graph. input values of previous models cannot be later models' output

    - _evaluate_single_iteration shall be a public method and to be tested
