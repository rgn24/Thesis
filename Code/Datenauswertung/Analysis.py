from util.Simulation import Simulation
import util.Visualization as vis
import util.Simulation as sim
import os

class Analysis:
    def __init__(self, simulations_path: str, exceptions: list, init_run: bool = True):
        self.simulations_path = simulations_path
        self.exceptions = exceptions
        self.init_run=init_run
        self.longest_sim_id = None
        self.all_dirs_abs = self.get_dirs()
        self.all_dirs_rel = [os.path.relpath(d, self.simulations_path) for d in self.all_dirs_abs]
        self.ignored_simulations = list()
        self.simulations = list()
        self.load_simulations()
        self.visualize = self.postprocess()
        
        # Assumed Simulation parameters global!
        self.h_first_element = 3e-10
        self.radius_capillary = 3e-9
        self.nu = 1e-3 #TODO CHECK IF CORRECT
        self.sigma = 0.072
        
        # Hier können weitere globale Variablen definiert werden

    def get_dirs(self):
        all_dirs = [os.path.join(self.simulations_path, d) for d in os.listdir(self.simulations_path) if os.path.isdir(os.path.join(self.simulations_path, d)) and d != "Plots"]
        return all_dirs
    
    def create_folder_plots(self):
        """creates a folder named Plots in a specified folder, if it not already exists."""
        check_folder = self.simulations_path + "/Plots/"
        if not os.path.exists(check_folder):
            os.makedirs(check_folder)
            print(f"folder: {check_folder} created.")
            
    def get_init_run(self):
        #TODO IMPLEMENTATION
        print("INIT CHECK NEEDS TO BE IMPLEMENTED")
        raise NotImplementedError
        #return self.init_run
        

    def load_simulations(self) -> None:
        longest_sim = 0
        
        for id_dir, dir in enumerate(self.all_dirs_abs):
            if dir.split(os.sep)[-1] in self.exceptions:
                self.ignored_simulations.append(dir)
                continue
            self.simulations.append(sim.Simulation(dir))
            print(type(self.simulations[-1].shape_df))
            # TODO not done yet! Foundation for support of LW (get longest Simulation to get the time data)
            if longest_sim < self.simulations[-1].shape_df[0]:
                longest_sim = self.simulations[-1].shape_df[0]
                self.longest_sim_id = id_dir
                
    def postprocess(self):
        time_series = self.simulations[self.longest_sim_id].df["Time"]
        print(len(time_series))
        print(self.simulations[self.longest_sim_id].name)
        visualize = vis.Visualization(self.simulations, dump_path=self.simulations_path, longest_id=self.longest_sim_id)
        
        
        #visualize.plot(xy=[["Time"], ["f_p", "f_t", "f_w"]], log_log="semilogx", save=False, show=True, n_th=1, y_limits=[0, 2e-9], monocolor=True)
        return visualize
        
    def get_info(self):
        return {"n-Simulaitons": len(self.simulations),"dirs": self.all_dirs_rel,"ignored Simulations ": self.ignored_simulations, "longest Simulation(id)": self.longest_sim_id, "path": self.simulations_path}

    def print_info(self):
        print("\n\nAnalysis Info: \n")
        for elem in self.get_info().keys():
            print(elem, ": ", self.get_info()[elem])
    # Hier können weitere Methoden für globale Analysen hinzugefügt werden
