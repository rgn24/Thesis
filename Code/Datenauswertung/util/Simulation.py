import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util.ErrorHandling import UnknownWritingError
import util.Computations as comp

from tqdm import tqdm

class Simulation:
    def __init__(self, dir_path) -> None:
        self.dir_path = dir_path
        self.name = os.path.basename(dir_path)
        self.shape = None
        self.init_run = True
        self.computed = False
        self.df = None
        self.history = self.set_history()
        print(self.history)
        
        self.preprocess()
        self.process_dataframe()
    
    def set_history(self):
        if "history" in os.listdir(self.dir_path):
            return True
        else:
            return False
            
        
    def get_state(self, files:list) -> None:
        for file in files:
            if file.endswith('merged.csv'):
                self.init_run = False
            if file.endswith('_computed.csv'):
                self.computed = True
                
    
    def set_data_info(self)-> None:
        self.shape = self.df.shape
        
    def merge_csv(self, files: list)-> None:
        """Merge all csv files of the provided list into one csv file and dumps it. Note: All duplicates will be deleted!

        Args:
            files (list): List with all Names of files path relative to the directory path
        """
        data_frames = []
        
        for id, file in enumerate(files):
            data_frames.append(pd.read_csv(os.path.join(self.dir_path, file)))
            #print(data_frames[id].head())

        # merge all dataframes
        merged_df = pd.concat(data_frames, axis=1)
        # clean up dataframe
        merged_df = merged_df.loc[:,~merged_df.columns.duplicated()].copy()
        self.df = merged_df
        try:
            merged_df.to_csv(os.path.join(f"{self.dir_path}/{self.name}_merged.csv"), index=False)
            print("Merged csv file written, to path: ", f"{self.dir_path}/{self.name}_merged.csv")
        except UnknownWritingError:
            print("Could not write merged csv file") 
            raise 
    
    def find_nearest(self, arr, value: float):
        arr = np.asarray(arr)
        idx = (np.abs(arr - value)).argmin()
        return arr[idx], idx
        
    def open_history_files(self):
        paths = {"wall": f"{self.dir_path}/history/0/wallForceswall.dat",
                    "energy": f"{self.dir_path}/history/0/energyDensitieswall.dat"}
        cols = {"wall": ["# Time", "pressureForceX", "pressureForceY", "pressureForceZ",
                            "viscousForceX", "viscousForceY", "viscousForceZ",
                            "capillaryForceX", "capillaryForceY", "capillaryForceZ"],
                "energy": ["time (s)", "Udown (m/s)", "eKinTot (j)",
                            "eDissTot (J)", "divDevRhoTot(N)",
                            "pdivDevRhoTot(N)"]}
        lists = {"wall": [[] for _ in range(len(cols["wall"]))],
                    "energy": [[] for _ in range(len(cols["energy"]))]}

        ids_rows = {"wall": [],
                    "energy": []}

        spacing = 1e-10
        delta = 5e-14
        temp_rows = []
        id_temp = []
        in_area = False
        time_step = spacing
        for elem in cols:
            print(f"opening {self.name}: {elem}")
            df = pd.read_csv(paths[elem], delimiter="\t", index_col=False)
            for index, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"Processing {elem}", leave=False):
                if np.abs(row[cols[elem][0]] - time_step) < delta:
                    in_area = True
                    temp_rows.append(row[cols[elem][0]])
                    id_temp.append(index)
                elif in_area:
                    _, id_nearest = self.find_nearest(temp_rows, time_step)
                    time_step += spacing
                    in_area = False
                    ids_rows[elem].append(id_temp[id_nearest])
                    temp_rows = []
                    id_temp = []
            time_step = spacing
            for id_list_rows, id_row in enumerate(ids_rows[elem]):
                for idl, line in enumerate(df):
                    lists[elem][idl].append(df.loc[id_row][line])
        #print(cols)
        if not lists["energy"][-1]:
            lists["energy"].pop()
            cols["energy"].pop()
        #    lists["energy"].pop()
        #    cols["energy"].pop()
        return cols["wall"], np.array(lists["wall"]).transpose(), cols["energy"], np.array(lists["energy"]).transpose()
        
    def preprocess_history(self) -> None:
        c_w, l_w, c_e, l_e = self.open_history_files()
        data_wall = pd.DataFrame(l_w, columns=c_w)
        data_wall.to_csv(f"{self.dir_path}/{self.name}_wall.csv", index=False)
        data_energy = pd.DataFrame(l_e, columns=c_e)
        data_energy.to_csv(f"{self.dir_path}/{self.name}_energy.csv", index=False)
            
    def get_csv_files(self):
        csv_files = [f for f in os.listdir(self.dir_path) if f.endswith('.csv')]
        if csv_files == []:
            raise Exception("No CSV files found")
        return csv_files
    
    def preprocess(self):
        csv_files = self.get_csv_files()
        if csv_files == []:
            raise Exception("No CSV files found")
        self.get_state(csv_files)
        
        if self.init_run:
            if self.history and not self.computed:
                self.preprocess_history()
                csv_files = self.get_csv_files()
            self.merge_csv(csv_files)
        else:
            self.df = pd.read_csv(os.path.join(self.dir_path, self.name + "_merged.csv"))
            print("read csv file: ", os.path.join(self.dir_path, self.name + "_merged.csv"))
            
    def process_dataframe(self):
        self.df.__class__ = type('CustomDataFrame', (comp.DataFrameUtilityMixin, pd.DataFrame), {})
        method_list = [method for method in dir(comp.DataFrameUtilityMixin) if method.startswith('__') is False]
        #print(method_list)
        
        # Nun können Sie die Methode wie gewünscht aufrufen
        self.df.compute_imbibition_height(160e-9)
        self.df.compute_velocity()
        self.df.compute_poiseuille_forces()
        self.df.compute_total_visc_force()
        self.df.compute_wedge_forces()
        
    
    def get_info(self):
        return {"name": self.name, "shape": self.shape, "path": self.dir_path, "cols": self.df.columns}
    
