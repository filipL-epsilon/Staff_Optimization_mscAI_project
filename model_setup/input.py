import json

def load_inputs(path):

    with open(path) as f:
        inst = json.load(f)

    # Sets
    h = inst["horizon"]
    H = range(1, h + 1)                              # time horizon {1, ..., h}
    Q = inst["qualifications"]                       # qualifications
    S = [s["name"] for s in inst["staff"]]           # staff
    J = [j["name"] for j in inst["jobs"]]            # projects

    # Staff parameters
    Q_i = {s["name"]: set(s["qualifications"]) for s in inst["staff"]}   # Q_i ⊆ Q
    V_i = {s["name"]: set(s["vacations"]) for s in inst["staff"]}        # V_i ⊆ H

    # Project parameters
    Q_j = {j["name"]: set(j["working_days_per_qualification"]) for j in inst["jobs"]}   # Q_j' ⊆ Q
    n = {(j["name"], k): days
        for j in inst["jobs"]
        for k, days in j["working_days_per_qualification"].items()}     # n[j, k]
    g = {j["name"]: j["gain"] for j in inst["jobs"]}                     # gain g_j
    d = {j["name"]: j["due_date"] for j in inst["jobs"]}                 # due date d_j
    c = {j["name"]: j["daily_penalty"] for j in inst["jobs"]}            # penalty c_j'

    return H, Q, S, J, Q_i, V_i, Q_j, n, g, d, c, h
