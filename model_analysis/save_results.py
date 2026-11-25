import json
from pathlib import Path


def save_results(results, data_path, solver_name):

    dataset_name = Path(data_path).stem

    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / f"{solver_name}_{dataset_name}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_path}")

    return output_path