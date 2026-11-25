### Epsilon solver for 2D constraints (profit + another) ###
import json

import gurobipy as gp
from gurobipy import GRB

from model_setup.input import load_inputs
from model_setup.variables import create_variables
from model_setup.constraints import add_constraints
from model_setup.objective_functions import objective_profit, objective_projects_late

def solver_epsilon_2D(path, secondary_objective="execution_time"):

    # 1. Inputs
    H, Q, S, J, Q_i, V_i, Q_j, n, g, d, c, h = load_inputs(path)

    # 2. Model
    m = gp.Model("solver_epsilon_2D")

    m.Params.TimeLimit = 60   # max 60 seconds per run
    m.Params.MIPGap = 0.03    # stop if profit gap within 3%

    # 3. Variables
    x, y, e, l, last_day, z, P, r, idx = create_variables(
        m, H, Q, S, J, Q_i, V_i, Q_j, h
    )

    # 4. Constraints
    add_constraints(
        m, x, y, e, l, last_day, z, P, r,
        idx, H, Q, S, J, Q_j, V_i, n, d
    )

    # 5. Primary objective
    m.setObjective(
        objective_profit(y, g, c, l, J),
        GRB.MAXIMIZE
    )

    # 6. Epsilon constraint

    secondary_objectives = {
    "execution_time": (last_day, max(H)),
    "projects_per_employee": (P, len(J)),
    "late_projects": (r.sum(), len(J))
    }

    obj, max_epsilon = secondary_objectives[secondary_objective]

    epsilon_constraint = m.addConstr(
        obj <= max_epsilon,
        name="epsilon_constraint"
    )

    # 7. Iterate over epsilon values

    results = []

    for epsilon in range(0, max_epsilon + 1):

        epsilon_constraint.RHS = epsilon

        m.optimize()

        if m.Status == GRB.OPTIMAL:

            results.append({
                "epsilon": epsilon,
                "profit": objective_profit(y, g, c, l, J).getValue(),
                "execution_time": last_day.X,
                "projects_per_employee": max(
                    sum(round(z[i, j].X) for j in J)
                    for i in S
                ),
                "late_projects": r.sum().getValue()
            })

    return m, results



  





