# Staff_Optimization_mscAI_project

Optimization of staff scheduling using decision modelling; educational purposes only.

## Suggested notations

- **Time horizon:** H = {1, …, h}, with h ∈ ℕ \ {0}.
- **Qualifications:** Q = {1, …, q} is the set of qualifications.
- **Staff:** S = {1, …, s} is the set of staff members.
  - Each staff member i ∈ S is characterized by:
    - a subset of qualifications Q_i ⊆ Q;
    - a subset of days off V_i ⊆ H.
- **Projects:** J = {1, …, m} is the set of projects.
  - Each project j ∈ J is characterized by:
    - a subset of required qualifications Q_j' ⊆ Q;
    - a number of person-days n_{j,k} ∈ ℕ for each required qualification k ∈ Q_j';
    - a gain g_j ∈ ℕ obtained when the project is completed;
    - a due date d_j ∈ H (present in the instance files);
    - a financial penalty c_j' ∈ ℕ per day of delay.

## Toy instance (`toy_instance.json`)

### Sets

| Set | Definition | Value |
|---|---|---|
| H (time horizon) | {1, …, h} | h = 5, so H = {1, 2, 3, 4, 5} |
| Q (qualifications) | {1, …, q} | q = 3, so Q = {A, B, C} |
| S (staff) | {1, …, s} | s = 3, so S = {Olivia, Liam, Emma} |
| J (projects) | {1, …, m} | m = 5, so J = {Job1, …, Job5} |

### Staff

| Name | Qualifications Q_i | Days off V_i |
|---|---|---|
| Olivia | A, B, C | none |
| Liam | A, B | 1 |
| Emma | C | 2 |

### Projects

Columns A, B and C give the required person-days n_{j,k}; "–" means the qualification is not required (k ∉ Q_j').

| Project | A | B | C | Gain g_j | Due date d_j | Penalty c_j' (per day) |
|---|---|---|---|---|---|---|
| Job1 | 1 | 1 | 1 | 20 | 3 | 3 |
| Job2 | 1 | 2 | – | 15 | 3 | 3 |
| Job3 | 1 | – | 2 | 15 | 4 | 3 |
| Job4 | – | 2 | 1 | 20 | 3 | 3 |
| Job5 | – | – | 2 | 10 | 5 | 3 |
