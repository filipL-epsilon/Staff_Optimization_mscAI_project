import gurobipy as gp
from gurobipy import GRB

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

def objective_projects_per_employee(m, z, S, J):
    # sum over projects and employees worked

    # introduce z from auxiliary_constraints

    # define a new variable that will hold the max no. projects worked on by any employee
    P = m.addVar(name = "max_projects")

    # which is the result of constraints on being at least as large as # projects for each employee
    for i in S:
        m.addConstr(P >= gp.quicksum(z[i,j]) for j in J)

    return P

def objective_projects_late(r, J):
    # return no. of projects that are late

    # r[j] is defined in auxiliary_constraints.py
    return gp.quicksum(r[j] for j in J)
