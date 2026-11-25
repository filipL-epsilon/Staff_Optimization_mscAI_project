from model_solvers.solver_multi import solver_multi
from model_analysis.save_results import save_results


def main():

    # Order: profit, execution time, workload, late projects
    combinations = {
        "profit_only":     (1, 0, 0, 0),
        "profit_emphasis": (4, 1, 1, 1),
        "equal_weights":   (1, 1, 1, 1),
        "time_emphasis":   (1, 4, 1, 1),
        "workload_emphasis": (1, 1, 4, 1),
        "lateness_emphasis": (1, 1, 1, 4),
    }

    for dataset in ["toy", "medium", "large"]:

        data_path = f"data/{dataset}_instance.json"
        all_results = {}

        for name, weights in combinations.items():

            print(f"\nRunning {dataset}: {name}")

            m, result = solver_multi(
                data_path,
                weights=weights,
                time_limit=60
            )

            all_results[name] = result

            # Save progress after each combination
            save_results(all_results, data_path, "multi")

            m.dispose()


if __name__ == "__main__":
    main()