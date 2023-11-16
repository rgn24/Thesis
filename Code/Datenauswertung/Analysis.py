from util.Simulation import Simulation
import util.Simulation as sim
import os

class Analysis:
    def __init__(self, simulations_path: str, exceptions: list, init_run: bool = True):
        self.simulations_path = simulations_path
        self.exceptions = exceptions
        self.init_run=init_run
        self.longest_sim_id = None
        self.all_dirs = self.get_dirs()
        self.simulations = list()
        self.load_simulations()
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
        for dir in self.all_dirs:
            if dir.split(os.sep)[-1] in self.exceptions:
                continue
            self.simulations.append(sim.Simulation(dir))
            print(type(self.simulations[-1].shape_df))
            # TODO not done yet! Foundation for support of LW (get longest Simulation to get the time data)
            if longest_sim < self.simulations[-1].shape_df[0]:
                longest_sim = self.simulations[-1].shape_df[0]
        self.longest_sim_id = longest_sim

    # Hier können weitere Methoden für globale Analysen hinzugefügt werden
