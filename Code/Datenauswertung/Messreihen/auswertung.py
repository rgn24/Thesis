import os
import pandas as pd

class UnknownWritingError(Exception):
    """Raised when a writing error occurs"""
    pass


class DataFrameUtilityMixin:
    def compute_velocity(self):
        # Ihre Berechnung hier. Zum Zwecke dieses Beispiels werde ich einfach eine neue Spalte "velocity" hinzufügen.
        # Sie können diesen Code an Ihre spezielle Logik anpassen.
        self["velocity"] = self["min(CACoordsX)"] * 2  # Beispielberechnung. Ersetzen Sie "some_column" durch den richtigen Spaltennamen.

class Simulation:
    def __init__(self, dir_path) -> None:
        self.dir_path = dir_path
        self.name = os.path.basename(dir_path)
        self.shape = None
        self.init_run = True
        self.df = None
        
        self.preprocess()
        self.process_dataframe()
        
    def get_init_run(self, files:list) -> None:
        for file in files:
            if file.endswith('merged.csv'):
                self.init_run = False
    
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
            print(data_frames[id].head())

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
    
    def preprocess(self):
        csv_files = [f for f in os.listdir(self.dir_path) if f.endswith('.csv')]
        if csv_files == []:
            raise Exception("No CSV files found")
        self.get_init_run(csv_files)
        
        if self.init_run:
            self.merge_csv(csv_files)
        else:
            self.df = pd.read_csv(os.path.join(self.dir_path, self.name + "_merged.csv"))
            print("read csv file: ", os.path.join(self.dir_path, self.name + "_merged.csv"))
            
    def process_dataframe(self):
        self.df.__class__ = type('CustomDataFrame', (DataFrameUtilityMixin, pd.DataFrame), {})
        
        # Nun können Sie die Methode wie gewünscht aufrufen
        self.df.compute_velocity()
        print(self.df.head())
    
    
    
    def get_info(self):
        return {"name": self.name, "length": self.length, "path": self.dir_path}
    
def get_dirs(base_directory):
    all_dirs = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    return all_dirs
    
def main():
    simulations_path = "./"
    exceptions = ["CA45"]
    all_dirs = get_dirs(simulations_path)
    print(all_dirs)
    simulations = []
    for dir in all_dirs:
        print(dir)
        if dir.split("/")[-1] in exceptions:
            continue
        simulations.append(Simulation(dir))
    
if __name__ == "__main__":
    main()
    
    