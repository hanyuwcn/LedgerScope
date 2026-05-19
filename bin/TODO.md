- go through each module with AI to discuss the interfaces and functionality 
- discuss on the project layout and description, readme 
- Have a general design doc 
- Implement each parts with test cases 
- Have a detailed design doc

- _evaluate_single_iteration shall be a public method and to be tested

- Have a description for each models, can be details like Evaluating COGS from purchasing price, orders and items

- test with same data on the old projects

- test with notebook to replicate same inputs

- review all the tests

- wrap up messages and variable keys


    - Add GUARDRAIL in the evaluate_chained_models to prevent used parameters was refreshing new values causing a conflict. 
      - This should more of a model sequence issue rather than parameter issue. 
      - Flow: Detecting a circle in a graph. input values of previous models cannot be later models' output

