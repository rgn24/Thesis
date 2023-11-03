import os
import util.Simulation as sim
import util.Visualization as vis
import util.Computations as comp

def get_dirs(base_directory):
    all_dirs = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d)) and d != "Plots"]
    return all_dirs

def create_folder_plots(path_: str = ""):
    """creates a folder named Plots in a specified folder, if it not already exists."""
    check_folder = path_ + "/Plots/"
    if not os.path.exists(check_folder):
        os.makedirs(check_folder)
        print(f"folder: {check_folder} created.")


def initialize_analysis(simulations_path: str="", exceptions: list=[])-> list:
    all_dirs = get_dirs(simulations_path)
    create_folder_plots(simulations_path)
    simulations = []
    for dir in all_dirs:
        if dir.split(os.sep)[-1] in exceptions:
            continue
        simulations.append(sim.Simulation(dir))
    return simulations

    
def main():
    simulations_path = "M:\Data_Plots\GammaLongRun"
    exceptions = ["CA45", "1_5e12"]
    
    simulations = initialize_analysis(simulations_path=simulations_path, exceptions=exceptions)
    print(f"loaded {len(simulations)} simulations")
    
    print(simulations[0].df["f_p"].head())
    viz = vis.Visualization(simulations, dump_path=simulations_path)
    viz.plot(xy=[["Time"], ["f_p", "f_t", "f_w"]], log_log="semilogx", save=False, show=True, n_th=1, y_limits=[0, 2e-9])
    
    
if __name__ == "__main__":
    main()
    
    