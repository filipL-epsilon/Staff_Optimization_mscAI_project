import gurobipy as gp 
from gurobipy import GRB

def add_constraints(
    m, x, y, e, l, last_day, z, P, r,
    idx, H, Q, S, J, Q_j, V_i, n, d
):
    
    # one staff member works on at most one project (and one skill) per day
    daily_assignment = m.addConstrs(
        (x.sum(i, t, "*", "*") <= 1 for i in S for t in H if t not in V_i[i]),
        name="daily_assignment",
    )

    # a project is either fully covered for each qualification (y=1) or not worked on at all (y=0)
    completed_project = m.addConstrs((x.sum("*", "*", j, k) == n[j,k] * y[j] for j in J for k in Q_j[j]), name="coverage",)

    # the completion day is at least every day someone works on the project
    end_day = m.addConstrs((e[j] >= t * x[i, t, j, k] for (i, t, j, k) in idx), name="end_day")

    # days late = completion day - due date (0 if on time)
    lateness = m.addConstrs((l[j] >= e[j] - d[j] for j in J), name="lateness")

    # --- auxiliary constraints (link the auxiliary variables to x, e and l) ---

    # last_day = max of the completion days
    makespan = m.addConstr(last_day == gp.max_(list(e.values())), name="makespan")

    # z[i,j] = OR of all x[i,t,j,k]: 1 as soon as employee i works one day on project j
    project_worked = {
        (i, j): m.addGenConstrOr(
            z[i, j],
            [x[i, t, j, k] for t in H for k in Q if (i, t, j, k) in x],
            name=f"project_worked[{i},{j}]",
        )
        for i in S for j in J
    }

    # P is at least the number of projects of each employee
    max_projects = m.addConstrs((P >= z.sum(i, "*") for i in S), name="max_projects")

    # r[j] = 0 -> no delay ; r[j] = 1 -> at least one day late (l is integer)
    late_off = m.addConstrs(((r[j] == 0) >> (l[j] == 0) for j in J), name="late_off")
    late_on  = m.addConstrs(((r[j] == 1) >> (l[j] >= 1) for j in J), name="late_on")