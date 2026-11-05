# Project brief specifies:
# 1) Maximize total profit realized
# 2) Minimize the actual project execution time
# 3) Minimize the number of projects an employee works on
# 4) Minimize the number of projects delivered late

def objective_profit(y,g,c,l):
    # sum over projects:
    # gain(g)*complete(y) - late penalty(c)*days late(l)
    return gp.quicksum(
        g[j]*y[j] - c[j]*l[j] for j in J
    )

def objective_execution_time(m,e):
    # sum over projects:
    # no. of days to complete
    M = m.addVar(name="last_day")
    m.addConstr(M == gp.max_(list(e.values())))
    return M

def objective_projects_per_employee(m,x):
    # sum over projects and employees worked

    # first check if employee 'i' works on project 'j'
    z = m.addVars(S, J, vtype=GRB.BINARY, name="project_worked")
    for i in S:
        for j in J:
            m.addGenConstrOr( # this sets z[i,j] to 1 if any of the x[..] are 1s for any day/project
                z[i,j],
                [x[i,t,j,k] for t in H for k in Q if (i,t,j,k) in x]
            )

    # define a new variable that will hold the max no. projects worked on by any employee
    P = m.addVar(name = "max_projects")

    # which is the result of constraints on being at least as large as # projects for each employee
    for i in S:
        m.addConstr(P >= gp.quicksum(z[i,j]) for j in J)

    return P

def objective_projects_late(m,l):
    # return no. of projects that are late

    # define variable r[j] to hold 0 if not late, 1 if late
    r = m.addVars(J, vtype=GRB.BINARY, name="late")

    # the constraints are = 0 if l[j] is zero, =1 if l[j] is positive
    for j in J:
        m.addGenConstrIndicator(r[j], 0, l[j] == 0)
        m.addGenConstrIndicator(r[j], 1, l[j] > 0)

    return gp.quicksum(r[j] for j in J)