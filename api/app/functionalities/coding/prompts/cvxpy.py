prompt_template = """
You're an expert programmer in a team of optimization experts. The goal of the team is to solve an optimization problem. Your task is to write cvxpy code for the {clauseType} of the problem.

Here's the {clauseType} we need you to write the code for:

-----
Description: {clauseDescription}
Formulation: {clauseFormulation}
-----

Here's the list of variables:

{relatedVariables}

Here's the list of parameters:

{relatedParameters}

Here's the problem summary:
{background}

Assume the parameters and variables are already defined and added to the model, cvxpy is imported as cp. Generate the code needed to define the {clauseType} and add it to the model accordingly.

Here is an example of code to add the objective, $\\max \\sum_{{i=1}}^{{N}} price_i x_i$ where the shape of both price and x is [N], to the model:

objective = cp.Maximize(cp.sum(cp.multiply(price, x)))

Here is an example of code to add a constraint, $\\forall i, SalesVolumes[i] \leq MaxProductionVolumes[i]$ where the shape of both SalesVolumes and MaxProductionVolumes is [N], to the model:

constraints.append(SalesVolumes <= MaxProductionVolumes)

- Only generate the code needed to define the {clauseType} and add it to the model accordingly. 
- Do not include any comments or explanations, unless no code is needed. If no code is needed, just return a comment saying "No code needed".
- Assume imports, parameters definitions, variable definitions, and other setup code is already written. You must not include any setup code.
- Even for simple constraints like non-negativity or sign constraints, include code to add them to the model explicitly (they are not added in the variable definition step).

Take a deep breath, and solve the problem step by step.
"""

import_code = "import cvxpy as cp"

# This code is used to get the solver information after the model is run. It should support all status (OPTIMAL, INFEASIBLE, UNBOUNDED, etc.) and store the objective value, variables, runtime, and iteration count in the solving_info dictionary.
get_info_code = """
import numpy as np
# Get solver information
solving_info = {}

if problem.status == cp.OPTIMAL:
    solving_info["status"] = "Optimal"
    solving_info["objective_value"] = float(problem.value) if problem.value is not None else None
    solving_info["variables"] = [
        {
            "symbol": var.name(),
            "value": float(var.value) if np.isscalar(var.value) else var.value.tolist() if hasattr(var.value, 'tolist') else list(var.value),
        }
        for var in problem.variables()
    ]
    solving_info["runtime"] = problem.solver_stats.solve_time
    solving_info["iteration_count"] = problem.solver_stats.num_iters
elif problem.status == cp.INFEASIBLE:
    solving_info["status"] = "Infeasible"
    solving_info["objective_value"] = None
    solving_info["variables"] = []
    solving_info["runtime"] = problem.solver_stats.solve_time
    solving_info["iteration_count"] = problem.solver_stats.num_iters
elif problem.status == cp.UNBOUNDED:
    solving_info["status"] = "Unbounded"
    solving_info["objective_value"] = None
    solving_info["variables"] = []
    solving_info["runtime"] = problem.solver_stats.solve_time
    solving_info["iteration_count"] = problem.solver_stats.num_iters
else:
    solving_info["status"] = f"Status: {problem.status}"
    solving_info["objective_value"] = None
    solving_info["variables"] = []
    solving_info["runtime"] = None
    solving_info["iteration_count"] = None
"""


def generate_variable_code(symbol, type, shape):
    type = type.upper()
    params = []
    if type == "INTEGER":
        params.append("integer=True")
    elif type == "BINARY":
        params.append("boolean=True")
    if shape:
        if len(shape) == 1:
            shape_str = shape[0]
        else:
            shape_str = f"({', '.join(shape)})"
        return f"{symbol} = cp.Variable({shape_str}, name='{symbol}'{', ' + ', '.join(params) if params else ''})"
    else:
        return f"{symbol} = cp.Variable(name='{symbol}'{', ' + ', '.join(params) if params else ''})"
