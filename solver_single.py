### Simple solver runs only the profit maximization condition ###
import json

import gurobipy as gp
from gurobipy import GRB

### TO ADD IMPORTS FOR INPUTS, VARIABLES, CONSTRAINTS -- WHEN TEAM IS DONE ###
from objective_functions import objective_profit
from auxiliary_constraints import add_auxiliary_constraints

def solver_single():
    # inputs
    ######### JULIEN ###########

    # start model
    m = gp.Model("solver_single")

    # variables and constraints
    ########### JULIEN / YONGYAN ##########
    
    # TODO: initialize variable required below
    y, e, f, l, r, z = add_auxiliary_constraints(
        m, x, S, J, H, Q_j, n, d
    )

    # objective
    m.setObjective(objective_profit(
        y,g,c,l ############# NEED TO ADD THE VARIABLES FROM ABOVE IN HERE WHEN COMPLETED / DEFINED
    ), GRB.MAXIMIZE)

    # run
    m.optimize()

    return m