import gurobipy as gp
from gurobipy import GRB

# add auxiliary variables and linking constraints to exsiting model
def add_auxiliary_constraints(m, x, S, J, H, Q_j, n, d):
    """
    Return:
        y: project selection
        e: completion day
        l: lateness in days
        r: late project indicator
        z: employee-project participation
    """

    # Selection variable
    y = m.addVars(J, vtype=GRB.BINARY, name="project selected")

    # Qualification coverage constraints
    for j in J:
        for k in Q_j[j]:
            m.addConstr(
                gp.quicksum(
                    x[i, t, j, k]
                    for i in S
                    for t in H
                    if (i, t, j, k) in x
                ) == n[j, k] * y[j],
                name=f"coverage_{j}_{k}"
            )

    # binary completion-day indicator variables, 0 or 1
    f = m.addVars(J, H, vtype=GRB.BINARY, name="finish")

    # Each selected project has exactly one completion day
    for j in J:
        m.addConstr(
            gp.quicksum(f[j, t] for t in H) == y[j],
            name=f"one_finish_day_{j}"
        )

    e = m.addVars(J, vtype=GRB.INTEGER, lb=0, ub=max(H), name="completion_day")

    for j in J:
        m.addConstr(
            e[j] == gp.quicksum(t * f[j, t] for t in H),
            name=f"completion_day_{j}"
        )

    # If a project finishes on day t, at least one assignment must occur on day t.
    for j in J:
        for t in H:
            m.addConstr(
                gp.quicksum(
                    x[i, t, j, k]
                    for i in S
                    for k in Q_j[j]
                    if (i, t, j, k) in x
                ) >= f[j, t],
                name=f"work_on_finish_day_{j}_{t}"
            )

    # no work after completion date
    for (i, t, j, k) in x.keys():
        m.addConstr(
            x[i, t, j, k] <= gp.quicksum(
                f[j, tau] for tau in H if tau >= t
            ),
            name=f"finish_after_work_{i}_{t}_{j}_{k}"
        )

    # binary variable for lateness, 0 or 1
    l = m.addVars(J, lb=0, vtype=GRB.INTEGER, name="lateness")

    for j in J:
        m.addConstr(l[j] >= e[j] - d[j])

    
    # binary late project indicator, 0 or 1
    r = m.addVars(J, vtype=GRB.BINARY, name="late_project")

    for j in J:
        # If r[j] = 0, then l[j] must be 0
        m.addConstr(
            l[j] <= max(H) * r[j],
            name=f"late_upper_{j}"
        )

        # If r[j] = 1, then l[j] must be at least 1
        m.addConstr(
            l[j] >= r[j],
            name=f"late_lower_{j}"
        )

    
    # employee-project participation variables
    z = m.addVars(S, J, vtype=GRB.BINARY, name="project_worked")

    for i in S:
        for j in J:
            # All possible assignments of employee i to project j
            assignments = [
                x[i, t, j, k]
                for t in H
                for k in Q_j[j]
                if (i, t, j, k) in x
            ]

            if assignments:
                m.addGenConstrOr(
                    z[i, j],
                    assignments,
                    name=f"participation_{i}_{j}"
                )
            else:
                m.addConstr(
                    z[i, j] == 0,
                    name=f"no_participation_{i}_{j}"
                )


    return y, e, f, l, r

