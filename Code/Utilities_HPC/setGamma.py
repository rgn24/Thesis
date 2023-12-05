import os
import re

def modify_files_in_latest_time_step(main_folder):
    # Durchsuchen der Hauptordners und Identifizieren der 'processor*' Ordner
    processor_folders = [d for d in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, d)) and d.startswith('processor')]
    print(processor_folders)
    for processor in processor_folders:
        processor_path = os.path.join(main_folder, processor)
        
        # Identifizieren der Zeitschritt-Ordner und Finden des letzten Zeitschritts
        time_step_folders = [d for d in os.listdir(processor_path) if os.path.isdir(os.path.join(processor_path, d)) and re.match(r'\d+\.\d+e[+-]\d+', d)]
        latest_time_step = max(time_step_folders, key=lambda x: float(x.split('e')[0]) * (10 ** float(x.split('e')[1])))

        # Pfad zum Ordner des letzten Zeitschritts
        latest_time_step_path = os.path.join(processor_path, latest_time_step)

        # Dateien, die geändert werden sollen
        files_to_modify = ['CWater', 'CAir']

        for file in files_to_modify:
            file_path = os.path.join(latest_time_step_path, file)
            if os.path.isfile(file_path):
                pass
                modify_file(file_path)

def modify_file(file_path):
    # Lesen der Datei und Suchen der 'alpha' Zeile
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Finden der Zeile, die 'alpha' enthält und Einfügen von 'Gamma 1.75e12;' vor dieser Zeile
    for i, line in enumerate(lines):
        if 'alpha' in line:
            lines.insert(i, '\t\tGamma 1.75e12;\n')
            break

    # Zurückschreiben der geänderten Datei
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Beispielhafter Aufruf der Funktion mit dem Pfad zum Hauptordner
# modify_files_in_latest_time_step('/path/to/M1_scripts') 
#modify_files_in_latest_time_step("/work/scratch/jk41zada/GammaMobility/M1_scripts")
# Hinweis: Sie müssen '/path/to/M1_scripts' durch den tatsächlichen Pfad zum Ordner 'M1_scripts' auf Ihrem System ersetzen.
sim_path = "/work/scratch/jk41zada/Equilibrium/M025/Gamma/GCA45_7e-8"
all_dirs = [os.path.join(sim_path, d) for d in os.listdir(sim_path) if os.path.isdir(os.path.join(sim_path, d))]


for simulation in all_dirs:
    print(simulation)
    modify_files_in_latest_time_step(simulation)

