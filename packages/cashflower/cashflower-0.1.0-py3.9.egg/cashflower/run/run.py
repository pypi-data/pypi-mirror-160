from cashflower.model import ModelVariable

import datetime
import importlib
import inspect
import pandas as pd


T_MAX = 1440

# User defines model functions
exec(open("model/policy.py").read())
module_name = "model.policy"
module = importlib.import_module(module_name)
module_functions = inspect.getmembers(module, inspect.isfunction)
module_functions = [func for func in module_functions if inspect.getmodule(func[1]) == module]

# Functions are turned into model variables
model_variables = []
for name, func in module_functions:
    exec(f"{name} = ModelVariable({name})")
    exec(f"model_variables.append({name})")

# Results are calculated
output = pd.DataFrame()
for model_variable in model_variables:
    output[model_variable.name] = [model_variable(t) for t in range(T_MAX)]

# Results are saved to file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{timestamp}.csv"
output.to_csv(filename)
