import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import sys


def analysis_epsilon_2D(data_path, solver_name="epsilon_2D"):

    # 1. Load results
    dataset_name = Path(data_path).stem
    results_path = Path("results") / f"{solver_name}_{dataset_name}.json"

    with open(results_path, "r") as f:
        all_results = json.load(f)

    # 2. Create charts
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, (obj, results) in zip(axes, all_results.items()):

        df = pd.DataFrame(results)

        if df.empty:
            continue

        # 3. Sort results
        df = df.sort_values(
            [obj, "profit"],
            ascending=[True, False]
        )

        # 4. Identify Pareto-optimal solutions
        pareto = df[
            df["profit"] > df["profit"].cummax().shift(
                1, fill_value=float("-inf")
            ) + 1e-6
        ]

        # 5. Plot results and Pareto frontier
        ax.scatter(df[obj], df["profit"],
                   alpha=0.4, label="All solutions")

        ax.plot(pareto[obj], pareto["profit"],
                "o-", label="Pareto frontier")

        ax.set_xlabel(obj.replace("_", " ").capitalize())
        ax.set_ylabel("Profit")
        ax.set_title(f"Profit vs {obj.replace('_', ' ')}")
        ax.grid(alpha=0.3)
        ax.legend()

    fig.suptitle(f"Pareto frontiers — {dataset_name}")
    plt.tight_layout()
    image_path = results_path.with_suffix(".png")
    fig.savefig(image_path, dpi=300, bbox_inches="tight")
    print(f"Charts saved to {image_path}")
    plt.show()


if __name__ == "__main__":

    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/toy_instance.json"
    analysis_epsilon_2D(data_path)