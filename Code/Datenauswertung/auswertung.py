import os
from Analysis import Analysis
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
    longest_sim = 0
    for dir in all_dirs:
        if dir.split(os.sep)[-1] in exceptions:
            continue
        simulations.append(sim.Simulation(dir))
        # TODO not done yet! Foundation for support of LW (get longest Simulation to get the time data)
        if longest_sim < simulations[-1].shape_df[0]:
            longest_sim = simulations[-1].shape_df[0]
    return simulations

    
def main(plot_list: list=[]):
    global_path = "M:\DataPlots_"
    viewed_simulations = ["CA15", "1_75e12", "CA45", "CA75"]
    naming = ["CA15", "GCA15"]
    #TODO add usage of file to load
    analysis = Analysis(simulations_path=global_path, viewed_simulations=viewed_simulations, naming=None)
    print(f"loaded {len(analysis.simulations)} simulations")
    #analysis.print_info()
    analysis.visualize.plot(xy=[["Time"], ["f_p", "f_t", "f_w"]], log_log="semilogx", save=True, show=True, n_th="log", y_limits=None, monocolor=True)
    analysis.visualize.plot(xy=[["Time"], ["imbibition_height"]], log_log=None, save=True, show=True, n_th=1, y_limits=None, monocolor=True, lw=15.0)
    
    
if __name__ == "__main__":
    main()
    