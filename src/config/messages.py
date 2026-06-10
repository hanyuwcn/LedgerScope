## STRING VALUE
### Break even analysis
BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER = "CROSSOVER_FOUND"
BREAK_EVEN_FEASIBILITY_UNREACHABLE = "UNREACHABLE"
BREAK_EVEN_FEASIBILITY_ALWAYS_FEASIBLE = "ALWAYS_FEASIBLE"

## LOGS
### Info
INFO_MONTE_CARLO_SIMULATION_START = "Initiating Monte Carlo analysis: {iterations} iterations targeted."
INFO_MONTE_CARLO_SIMULATION_FINISH = "Monte Carlo simulation completed. Captured {size} records."

### ERROR
ERROR_VARIABLE_CONSTRUCTION_ERROR = ("Invalid argument combination. You must provide either: \n "
                                     "1. All three (min, max, expect)\n "
                                     "2. Only 'expect'\n "
                                     "3. Only 'min' and 'max'")

ERROR_VARIABLE_NOT_SETUP = "{var} not setup"
ERROR_VARIABLE_TYPE_NOT_SUPPORT = "Value type not supported"
ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE = "Variable(s) not setup: {msg}"
ERROR_VARIABLE_NOT_MONOTONIC_EFFECT = "The performance curve of {result} is non-monotonic for {factor}."

ERROR_PIPELINE_TOPOLOGY_ORDER_VIOLATION = (
    "Pipeline Order Violation: '{variable_name}' is generated as an output by '{current_model}', "
    "but it was already consumed as a required input upstream by '{earlier_model}'. "
    "Please move '{current_model}' earlier in your pipeline sequence.")
