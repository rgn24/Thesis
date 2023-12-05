import os

def modify_control_dict(file_path, end_time=None, max_co=None):
    """Modify the controlDict file based on the given values."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modify the lines for endTime and maxCo if values are given
    if end_time:
        for idx, line in enumerate(lines):
            if line.strip().startswith('endTime'):
                lines[idx] = f"endTime         {end_time};\n"
                
    if max_co:
        for idx, line in enumerate(lines):
            if line.strip().startswith('maxCo'):
                lines[idx] = f"maxCo           {max_co};\n"

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)



def main():
    starting_path = input("Enter the path to start from (or press Enter to use the current directory): ")
    if not starting_path:
        print("HELLO")
        starting_path = '.'
    end_time = input("Enter new value for endTime (or press Enter to skip): ")
    max_co = input("Enter new value for maxCo (or press Enter to skip): ")
    
    print(starting_path)
    # Determine if we are in a simulation folder
    if os.path.isdir(os.path.join(starting_path, 'system')) and os.path.isfile(os.path.join(starting_path, 'system/controlDict')):
        file_path = os.path.join(starting_path, 'system/controlDict')
        print(f"Modifying: {file_path}")
        modify_control_dict(file_path, end_time if end_time else None, max_co if max_co else None)
    else:
        # Not in a Simulations folder -> search for subfolders and change them. 
        for root, dirs, files in os.walk(starting_path):
            if 'controlDict' in files:
                file_path = os.path.join(root, 'controlDict')
                print(f"Modifying: {file_path}")
                modify_control_dict(file_path, end_time if end_time else None, max_co if max_co else None)

main()
