from model_solvers.solver_single import solver_single
from model_solvers.solver_epsilon_2D import solver_epsilon_2D
from model_analysis.save_results import save_results

data_path = "data/medium_instance.json"

def main():
    # m, results = solver_single(data_path)
    # print(results)

    ############## 2D EPSILON SOLVERS #########

    objectives = [
    "execution_time",
    "projects_per_employee",
    "late_projects"
    ]

    all_results = {}

    for obj in objectives:
        m, results = solver_epsilon_2D(data_path, obj)
        all_results[obj] = results

    save_results(all_results, data_path, "epsilon_2D")


if __name__ == "__main__":
    main()





