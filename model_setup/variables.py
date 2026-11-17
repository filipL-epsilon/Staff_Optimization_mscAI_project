import gurobipy as gp 
from gurobipy import GRB

def create_variables(m, H, Q, S, J, Q_i, V_i, Q_j, h):

    # Initialize assignment decision variables.

    # x[i,t,j,k]: only valid combinations (qualified, not on vacation, project needs k)
    idx = [(i, t, j, k)
        for i in S
        for t in H if t not in V_i[i]
        for j in J
        for k in Q_j[j] & Q_i[i]]

    # matrix of peapole, job, skill, day
    x = m.addVars(idx, vtype=GRB.BINARY, name="x")

    # auxilliary variable: project j completed in horizon
    y = m.addVars(J, vtype=GRB.BINARY, name='y')

    # completion day of the project
    e = m.addVars(J, vtype=GRB.INTEGER, lb=0, ub=h, name='e')

    # number of days late of the project
    l = m.addVars(J, vtype=GRB.INTEGER, lb=0, name='l')

    # last_day: last completion day over all projects (makespan)
    last_day = m.addVar(vtype=GRB.INTEGER, lb=0, ub=h, name="last_day")

    # z[i,j] = 1 if employee i works at least one day on project j
    z = m.addVars(S, J, vtype=GRB.BINARY, name="project_worked")

    # P: max number of projects worked on by any single employee
    P = m.addVar(vtype=GRB.INTEGER, lb=0, ub=len(J), name="max_projects")

    # r[j] = 1 if project j is delivered late, 0 otherwise
    r = m.addVars(J, vtype=GRB.BINARY, name="late")

    return x, y, e, l, last_day, z, P, r, idx