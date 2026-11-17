from model_solvers.solver_single import solver_single
####### ADD OTHER SOLVERS AT SOME POINT ##########

data_path = "data.toy_instance.json"

def main():
    m, results = solver_single(data_path)
    print(results)
    ##### INSERT OTHER SOLVERS WHEN READY ##########

if __name__ == "__main__":
    main()