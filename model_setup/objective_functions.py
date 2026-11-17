import gurobipy as gp 
from gurobipy import GRB

# Project brief specifies:
# 1) Maximize total profit realized
# 2) Minimize the actual project execution time
# 3) Minimize the number of projects an employee works on
# 4) Minimize the number of projects delivered late
# The auxiliary variables/constraints are defined above: these functions only return an expression.

def objective_profit(y, g, c, l, J):
    # gain of completed projects - late penalty * days late
    return gp.quicksum(g[j] * y[j] - c[j] * l[j] for j in J)

def objective_execution_time(last_day):
    # last completion day over all projects
    return last_day

def objective_projects_per_employee(P):
    # max number of projects worked on by any employee
    return P

def objective_projects_late(r):
    # number of projects delivered late
    return r.sum()