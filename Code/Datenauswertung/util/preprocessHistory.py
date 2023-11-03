import numpy as np 
import pandas as pd

def find_nearest(arr, value: float):
    arr = np.asarray(arr)
    idx = (np.abs(arr - value)).argmin()
    return arr[idx], idx

def open_history_files(self):
    paths = {"wall": f"{self.path_folder}history/0/wallForceswall.dat",
                "energy": f"{self.path_folder}history/0/energyDensitieswall.dat"}
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
        print(f"opening {name}: {elem}")
        df = pd.read_csv(paths[elem], delimiter="\t", index_col=False)
        for index, row in df.iterrows():
            if np.abs(row[cols[elem][0]] - time_step) < delta:
                in_area = True
                temp_rows.append(row[cols[elem][0]])
                id_temp.append(index)
            elif in_area:
                _, id_nearest = find_nearest(temp_rows, time_step)
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

def preprocess_history(self):
    if self.bool_first_run:
        c_w, l_w, c_e, l_e = self.open_history_files()
        data_wall = pd.DataFrame(l_w, columns=c_w)
        data_wall.to_csv(f"{self.path_folder}{self.name}_wall.csv", index=False)
        data_energy = pd.DataFrame(l_e, columns=c_e)
        data_energy.to_csv(f"{self.path_folder}{self.name}_energy.csv", index=False)
        self.merge_dataframes(data_wall, data_energy)
