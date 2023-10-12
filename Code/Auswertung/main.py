import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os



def open_csv(path_to_file):
    df = pd.read_csv(path_to_file, sep = ",")
    return df

def get_files(path_to_files):
    files = os.listdir(path_to_files)
    n_files = len(files)
    return files, n_files



def plot_simulations(simulations,x="Time", y="max(coordsX)"):
    for id_s, simulation in enumerate(simulations):
        print(simulations[id_s].head())
        plt.scatter(simulation[x], 160e-9-simulation[y], label = "Simulation " + str(id_s))
        plt.loglog()
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = 1e-9 + 0.5 * x_vals
    y_vals1 = 1e-9 + 1 * x_vals
    plt.plot(x_vals, y_vals, '--')
    plt.plot(x_vals, y_vals1, '--')
    plt.grid(True, which="both", ls="-")
    plt.show()

if __name__ == "__main__":
    simulations = []
    sim_dict = {}
    path_to_files = "Code/Auswertung/files/"
    files, n_files = get_files(path_to_files)
    for id_file, file_name,  in enumerate(files):
        sim_dict[id_file] = [file_name]
        simulations.append(open_csv(path_to_files + file_name))
    
    
    plot_simulations(simulations)
    

    
    

