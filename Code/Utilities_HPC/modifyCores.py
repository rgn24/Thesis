import os

def modify_decomposeParDict(file_path, number_of_subdomains, n_values):
    """Modify the decomposeParDict file based on the given values."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if line.strip().startswith('numberOfSubdomains'):
            lines[idx] = f"numberOfSubdomains {number_of_subdomains};\n"
        elif line.strip().startswith('n'):
            lines[idx] = f"    n       ( {n_values[0]} {n_values[1]} {n_values[2]} );\n"

    with open(file_path, 'w') as file:
        file.writelines(lines)

def modify_submit_sh(file_path, number_of_subdomains, simulation_name, simulation_path):
    """Modify the submit.sh file based on the given values."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    for idx, line in enumerate(lines):
        if line.strip().startswith('#SBATCH -J'):
            lines[idx] = f"#SBATCH -J {simulation_name}\n"
        if line.strip().startswith('#SBATCH -n'):
            lines[idx] = f"#SBATCH -n {number_of_subdomains}\n"
        if line.strip().startswith('cd'):
            lines[idx] = f"cd {simulation_path}\n"
        if line.strip().startswith('mpirun'):
            lines[idx] = f"mpirun -np {number_of_subdomains} phaseFieldFoam -parallel >log.phaseFieldFoam\n"

    print("file modified")
    with open(file_path, 'w') as file:
        file.writelines(lines)

def main_modify_files(starting_path,  number_of_subdomains, n_values, simulation_name):

    modify_decomposeParDict(os.path.join(starting_path, 'system/decomposeParDict'), number_of_subdomains, n_values)
    #simulation_path = input("Enter the path for the simulation (used in submit.sh): ")
    modify_submit_sh(os.path.join(starting_path, 'submit.sh'), number_of_subdomains, simulation_name, starting_path)

    print("Files modified successfully!")


def get_file_paths(starting_path):
    if os.path.isdir(os.path.join(starting_path, 'system')) and os.path.isdir(os.path.join(starting_path, '0.orig')) and os.path.isdir(os.path.join(starting_path, 'constant')):
        file_path = {"submit.sh": os.path.join(starting_path, 'submit.sh'), 
                     "decomposeParDict": os.path.join(starting_path, "system/decomposeParDict")}
    return file_path

def main():
    starting_path = input("Enter the path to start from (or press Enter to use the current directory): ")
    if not starting_path:
        starting_path = '.'
    number_of_subdomains = int(input("Enter the number of cores (numberOfSubdomains): "))

    while True:
        n_values = list(map(int, input("Enter the partitioning in x, y, z (e.g., 2 2 4): ").split()))
        if len(n_values) == 3 and (n_values[0] * n_values[1] * n_values[2] == number_of_subdomains):
            break
        else:
            print("Invalid partitioning! The product of the numbers should equal the numberOfSubdomains. Try again.")
    simulation_name = input("Enter the name for the simulation (used in submit.sh): ")

    if os.path.isdir(os.path.join(starting_path, 'system')) and os.path.isdir(os.path.join(starting_path, '0.orig')) and os.path.isdir(os.path.join(starting_path, 'constant')):
        simulation_name = "unknown"
        print("CURRENTLY NOT WORKING!!! PATH ERROR!")
        main_modify_files(starting_path, number_of_subdomains, n_values, simulation_name)
    else:
        count = 0
        for root, dirs, files in os.walk(starting_path):
            if os.path.isdir(os.path.join(root, 'system')) and os.path.isdir(os.path.join(root, '0.orig')) and os.path.isdir(os.path.join(root, 'constant')):
                simulation_name = root.split("/")[-1]
                main_modify_files(root, number_of_subdomains, n_values, simulation_name)
                count += 1
main()