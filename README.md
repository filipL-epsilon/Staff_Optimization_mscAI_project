# Staff_Optimization_mscAI_project
Optimization of staff scheduling using decision modelling; educational purposes only.

# Suggested notations:
Time horizon: H = {1, …, h}, with h ∈ ℕ \ {0}.
Qualifications: Q = {1, …, q} is the set of qualifications.
Staff: S = {1, …, s} is the set of staff members.
For each i ∈ S, a staff member i is characterized by:
- a subset of qualifications Q_i ⊆ Q;
- a subset of days off V_i ⊆ H.
Projects: J = {1, …, m} is the set of projects.
For each j ∈ J, a project j is characterized by:
- a subset of required qualifications Q_j' ⊆ Q;
- a number of person-days n_{j,k} ∈ ℕ for each required qualification k ∈ Q_j';
- a gain g_j ∈ ℕ obtained when the project is completed;
- a financial penalty c_j' ∈ ℕ per day of delay.
