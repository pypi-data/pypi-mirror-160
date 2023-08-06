from cashflower.model import ModelVariable

import datetime
import importlib
import inspect
import pandas as pd


T_MAX = 1440

exec(open("model/policy.py").read())


module_name = "model.policy"
module = importlib.import_module(module_name)
module_functions = inspect.getmembers(module, inspect.isfunction)
module_functions = [func for func in module_functions if inspect.getmodule(func[1]) == module]

model_variables = []
for name, func in module_functions:
    exec(f"{name} = ModelVariable({name})")
    exec(f"model_variables.append({name})")

output = pd.DataFrame()
for model_variable in model_variables:
    output[model_variable.name] = [model_variable(t) for t in range(T_MAX)]


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{timestamp}.csv"
output.to_csv(filename)
