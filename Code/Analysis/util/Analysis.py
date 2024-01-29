import os
from typing import Optional
import util.Visualization as vis
import util.Simulation as sim

class Analysis:
    def __init__(self, path: str, viewed: list, naming: Optional[list] = None):
        self.path = path
        self.viewed = viewed
        self.naming = self.set_naming(naming)
        print("Naming Viewed", self.naming, self.viewed)


        self.all_dirs_abs = self.get_dirs()
        self.all_dirs_rel = [os.path.relpath(d, self.path) for d in self.all_dirs_abs]
        self.viewed_abs_path = self.set_abs_viewed_path()
        print("ABS", self.viewed_abs_path)
        self.ignored_simulations = []
        self.simulations = []

        # constants
        self.h_first_element = 3e-10
        self.radius_capillary = 3e-9
        self.nu = 1e-3  # TODO CHECK IF CORRECT
        self.sigma = 0.072

        # inits
        self.create_folder_plots()
        self.geom = self.set_geom()
        self.longest_sim_id = None
        self.init_run = True


    def print_info(self):
        dict_info = {"path": self.path, "viewed": self.viewed, "naming": self.naming, "geom": self.geom}
        for key in dict_info:
            print(f"{key}: {dict_info[key]}")

    def set_abs_viewed_path(self):
        viewed_abs = []
        for folder in self.viewed:
            viewed_abs.append(os.path.join(self.path, folder))
        return viewed_abs

    def set_naming(self, naming: Optional[list] = None):
        if naming is None:
            print("VIEWED", self.viewed)
            return self.viewed
        else:
            return naming

    def get_dirs(self):
        all_dirs = [os.path.join(self.path, d) for d in os.listdir(self.path) if
                    os.path.isdir(os.path.join(self.path, d)) and d != "Plots"]
        # print(all_dirs)
        return all_dirs

    def create_folder_plots(self):
        """creates a folder named Plots in a specified folder, if it not already exists."""
        check_folder = self.path + "/Plots/"
        if not os.path.exists(check_folder):
            os.makedirs(check_folder)
            print(f"folder: {check_folder} created.")

    def set_geom(self) -> dict:
        LONGGEOM = ["R6_Equi", "R4_Equi", "R3_Equi"]
        radius = 3e-9
        height = 160e-9
        geom = []
        for simulation in self.viewed:
            print(simulation)
            if simulation in LONGGEOM:
                height = 380e-9
                if simulation == "R6_Equi":
                    radius = 6e-9
                elif simulation == "R4_Equi":
                    radius = 4e-9
                elif simulation == "R3_Equi":
                    radius = 3e-9
            geom.append({"height": height, "radius": radius})
        return geom

    def load_simulations(self) -> None:
        longest_sim = 0
        loaded_id = 0
        for id_dir, dir in enumerate(self.viewed_abs_path):
            self.simulations.append(sim.Simulation(dir_path=dir, name_plot=self.naming[id_dir], geom=self.geom[id_dir]))
            if longest_sim < self.simulations[-1].shape_df[0]:
                longest_sim = self.simulations[-1].shape_df[0]
                self.longest_sim_id = id_dir
            loaded_id += 1
            #self.simulations[-1].print_info()

    def postprocess(self):
        #time_series = self.simulations[self.longest_sim_id].df["Time"]
        visualize = vis.Visualization(self.simulations, dump_path=self.path, longest_id=self.longest_sim_id)
        return visualize



