import os
import pandas as pd

class Simulation:
    def __init__(self, dir_path) -> None:
        self.path = dir_path
        self.name = os.path.basename(dir_path)
        self.length = 0
        
    def preprocess(self):
        csv_files = [f for f in os.listdir(self.path) if f.endswith('.csv')]
        data_frames = []
        
        for id, file in enumerate(csv_files):
            data_frames.append(pd.read_csv(os.path.join(self.path, file)))
            print(data_frames[id].head())

        # Alle DataFrames in der Liste zu einem DataFrame zusammenfügen
        merged_df = pd.concat(data_frames, axis=0, ignore_index=True)
        print("FINAL", merged_df.head())
    
    
    def get_info(self):
        return {"name": self.name, "length": self.length, "path": self.dir_path}
    
def get_dirs(base_directory):
    all_dirs = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    return all_dirs
    
def main():
    simulations_path = "Messreihen/"
    all_dirs = get_dirs(simulations_path)
    print(all_dirs)
    simulations = []
    for dir in all_dirs:
        simulation = Simulation(dir)
        print(simulation.name)
        simulation.preprocess()
    
if __name__ == "__main__":
    main()
    
    