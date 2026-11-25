### Solver running on multiple objective functions with weights ###
import json

import gurobipy as gp
from gurobipy import GRB

from model_setup.input import load_inputs
from model_setup.variables import create_variables
from model_setup.constraints import add_constraints
from model_setup.objective_functions import objective_profit, objective_projects_late

def solver_multi(path, weights, time_limit=60):

    # 1. Inputs
    H, Q, S, J, Q_i, V_i, Q_j, n, g, d, c, h = load_inputs(path)

    # 2. Model
    m = gp.Model("solver_multi")
    m.Params.TimeLimit = time_limit
    m.Params.MIPGap = 0.01

    # 3. Variables
    x, y, e, l, last_day, z, P, r, idx = create_variables(
        m, H, Q, S, J, Q_i, V_i, Q_j, h
    )

    # 4. Constraints
    add_constraints(
        m, x, y, e, l, last_day, z, P, r,
        idx, H, Q, S, J, Q_j, V_i, n, d
    )

    # 5. Objectives
    # scale the objectives to be comparable when weighting
    # weights inputted from the main

    w_profit, w_time, w_workload, w_late = weights

    profit = objective_profit(y, g, c, l, J)

    profit_scale = max(1, sum(g.values()))
    time_scale = max(1, h)
    count_scale = max(1, len(J))

    m.setObjective(
        w_profit * profit / profit_scale
        - w_time * last_day / time_scale
        - w_workload * P / count_scale
        - w_late * r.sum() / count_scale,
        GRB.MAXIMIZE
    )


    # 6. Solve

    m.optimize()

    status_names = {
        GRB.OPTIMAL: "Optimal within tolerance",
        GRB.TIME_LIMIT: "Time limit",
        GRB.INFEASIBLE: "Infeasible",
        GRB.INTERRUPTED: "Interrupted",
    }

    results = {
        "weights": {
            "profit": w_profit,
            "execution_time": w_time,
            "projects_per_employee": w_workload,
            "late_projects": w_late,
        },
        "runtime": m.Runtime,
        "status": status_names.get(m.Status, str(m.Status)),
        "has_solution": m.SolCount > 0,
        "profit": None,
        "execution_time": None,
        "projects_per_employee": None,
        "late_projects": None,
        "weighted_score": None,
        "weighted_gap": None,
    }


    if m.SolCount > 0:

        # Calculate actual metrics from the schedule
        completion = {j: 0 for j in J}
        employee_projects = {i: set() for i in S}

        for i, t, j, k in idx:
            if x[i, t, j, k].X > 0.5:
                completion[j] = max(completion[j], t)
                employee_projects[i].add(j)

        gap = m.MIPGap

        results.update({
            "profit": profit.getValue(),
            "execution_time": max(completion.values(), default=0),
            "projects_per_employee": max(
                (len(projects) for projects in employee_projects.values()),
                default=0
            ),
            "late_projects": sum(
                completion[j] > d[j] for j in J
            ),
            "weighted_score": m.ObjVal,
            "weighted_gap": gap if gap < float("inf") else None,
        })

    return m, results


