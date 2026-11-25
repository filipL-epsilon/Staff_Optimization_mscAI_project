### Simple solver runs only the profit maximization condition ###
import json

import gurobipy as gp
from gurobipy import GRB

from model_setup.input import load_inputs
from model_setup.variables import create_variables
from model_setup.constraints import add_constraints
from model_setup.objective_functions import objective_profit, objective_projects_late

def solver_single(path):

    # 1. Inputs
    H, Q, S, J, Q_i, V_i, Q_j, n, g, d, c, h = load_inputs(path)

    # 2. Model
    m = gp.Model("solver_single")

    # 3. Variables
    x, y, e, l, last_day, z, P, r, idx = create_variables(
        m, H, Q, S, J, Q_i, V_i, Q_j, h
    )

    # 4. Constraints
    add_constraints(
        m, x, y, e, l, last_day, z, P, r,
        idx, H, Q, S, J, Q_j, V_i, n, d
    )

    # 5. Objective
    m.setObjective(
        objective_profit(y, g, c, l, J),
        GRB.MAXIMIZE
    )

    # 6. Solve
    m.optimize()

    if m.SolCount > 0:
        results = {
            "profit": objective_profit(y, g, c, l, J).getValue(),
            "execution_time": last_day.X,
            "projects_per_employee": P.X,
            "late_projects": objective_projects_late(r).getValue()
        }

        return m, results

    return m, None

