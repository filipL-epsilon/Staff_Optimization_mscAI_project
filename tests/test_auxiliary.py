import json, pytest

import gurobipy as gp
from gurobipy import GRB

from auxiliary_constraints import add_auxiliary_constraints

def build_test_model():

    # load toy_instance dataset and initilize core variables
    with open("data/toy_instance.json") as file:
        tyinst = json.load(file)

    h = tyinst["horizon"]
    H = range(1, h + 1)
    S = [s["name"] for s in tyinst["staff"]]
    J = [j["name"] for j in tyinst["jobs"]]

    Q_i = {
        s["name"]: set(s["qualifications"])
        for s in tyinst["staff"]
    }
    V_i = {
        s["name"]: set(s["vacations"])
        for s in tyinst["staff"]
    }
    Q_j = {
        j["name"]: set(j["working_days_per_qualification"])
        for j in tyinst["jobs"]
    }

    # total days of skill k job j needs
    n = {
        (j["name"], k): days
        for j in tyinst["jobs"]
        for k, days in j["working_days_per_qualification"].items()
    }
    g = {
        j["name"]: j["gain"] 
        for j in tyinst["jobs"]
    }
    d = {
        j["name"]: j["due_date"] 
        for j in tyinst["jobs"]
    }
    p = {
        j["name"]: j["daily_penalty"] 
        for j in tyinst["jobs"]
    }

    # create model
    m = gp.Model("test_auxiliary")

    idx = [
        (i, t, j, k)
        for i in S
        for t in H if t not in V_i[i]
        for j in J
        for k in Q_j[j] & Q_i[i]
    ]

    x = m.addVars(idx, vtype=GRB.BINARY, name="x")

    # each employee works on at most one task per day
    for i in S:
        for t in H:
            m.addConstr(
                gp.quicksum(
                    x[cur_i, cur_t, j, k]
                    for cur_i, cur_t, j, k in x.keys()
                    if cur_i == i and cur_t == t
                ) <= 1
            )

    y, e, f, l, r, z = add_auxiliary_constraints(
        m, x, S, J, H, Q_j, n, d
    )

    return m, x, y, e, f, l, r, z, J, S, H, d, g, p


def test_auxiliary_constraints():

    m, x, y, e, f, l, r, z, J, S, H, d, g, p = build_test_model()

    # try to maximize profit
    m.setObjective(
        gp.quicksum(
            g[j] * y[j] - p[j] * l[j]
            for j in J
        ),
        GRB.MAXIMIZE
    )

    m.optimize()

    if m.Status != GRB.OPTIMAL:
        raise RuntimeError(f"Optimization status: {m.Status}")

    # verify results
    for j in J:
        assignments = [
            (i, t, k) # staff i works on job j with skill k on day t
            for i, t, cur_j, k in x.keys()
            if cur_j == j and x[i, t, cur_j, k].X > 0.5
        ]

        expected_e = max((t for i, t, k in assignments), default=0)
        expected_l = max(0, expected_e - d[j])
        expected_r = int(expected_l > 0)

        assert round(e[j].X) == expected_e
        assert round(l[j].X) == expected_l
        assert round(r[j].X) == expected_r
        assert round(y[j].X) == int(bool(assignments))

        print(
            f"{j}: selected={round(y[j].X)}, "
            f"completion={round(e[j].X)}, "
            f"lateness={round(l[j].X)}, "
            f"late={round(r[j].X)}"
        )

    for i in S:
        for j in J:
            worked = any(
                ii == i and jj == j and x[ii, t, jj, k].X > 0.5
                for ii, t, jj, k in x.keys()
            )
            assert round(z[i, j].X) == int(worked)


def test_forced_lateness():

    m, x, y, e, f, l, r, z, J, S, H, d, g, p = build_test_model()

    # TODO: implement a Gurobi test for forced lateness.
    pytest.skip("Not implemented yet。")

    pass