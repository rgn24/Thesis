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
    longest_sim = 0
    for dir in all_dirs:
        if dir.split(os.sep)[-1] in exceptions:
            continue
        simulations.append(sim.Simulation(dir))
        print(type(simulations[-1].shape_df))
        # TODO not done yet! Foundation for support of LW (get longest Simulation to get the time data)
        if longest_sim < simulations[-1].shape_df[0]:
            longest_sim = simulations[-1].shape_df[0]
    print(f"longest simulation has {longest_sim} timesteps")
    return simulations

    
def main(plot_list: list=[]):
    #simulations_path = "M:\Data_Plots\GammaLongRun"
    simulations_path = "M:\Data_Plots\GammaLongRunCO"
    #simulations_path = "M:\Data_Plots\MobilityStudyEQUI"
    #simulations_path = "M:\Data_Plots\MobilityStudyGAMMA"
    exceptions = ["CA45", "GM1", "GM2", "GM025"]
    
    simulations = initialize_analysis(simulations_path=simulations_path, exceptions=exceptions)
    print(f"loaded {len(simulations)} simulations")
    
    viz = vis.Visualization(simulations, dump_path=simulations_path)
    
    viz.plot(xy=[["Time"], ["f_p", "f_t", "f_w"]], log_log="semilogx", save=False, show=True, n_th=1, y_limits=[0, 2e-9], monocolor=True)
    viz.plot(xy=[["Time"], ["imbibition_height"]], log_log="loglog", save=False, show=True, n_th=1, y_limits=None, monocolor=True)
    viz.plot(xy=[["Time"], ["ca_first_element"]], log_log=None, save=False, show=True, n_th=1, y_limits=None, monocolor=True)
    
    
    #for plots in plot_list:
    #    viz.plot(xy=plots, log_log="semilogx", save=False, show=True, n_th=1, y_limits=None, monocolor=True)
    
    
if __name__ == "__main__":
    #plotting_list = [[["Time"], ["f_p", "f_t", "f_w"]], 
    #                 [["Time"], ["imbibition_height"]]]
    main()
    
    