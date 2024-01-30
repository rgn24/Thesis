import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
print(script_directory)

from util.Analysis import Analysis

#comparison of Equilibrium and out of equilibrium (CA15)
gamma_comp = ["CA15", "GM025"]
gamma_naming = [r"\textbf{equilibrium}", r"\textbf{out of equilibrium}"]
gamma_naming_save_name = ["gammaComp_Forces", "gamma_Comp_imbibition_subplots"]
gamma_comp_dict = {"viewed": gamma_comp, "naming": gamma_naming, "save_name": gamma_naming_save_name}

#comparison of out of equilibrium and different values for gamma
gamma_study_comp = ["M16_1_0e13", "M16_2_0e12", "M16_1_75e12", "M16_1_5e12"]
gamma_study_naming = [r"\boldmath{$1.00\cdot 10^{13}$}", r"\boldmath{$2.00\cdot 10^{12}$}", r"\boldmath{$1.75\cdot 10^{12}$}", r"\boldmath{$1.50\cdot 10^{12}$}"]
gamma_study_naming_save_name = ["gammaStudy_Forces", "gamma_Study_imbibition_subplots"]
gamma_study_comp_dict = {"viewed": gamma_study_comp, "naming": gamma_study_naming, "save_name": gamma_study_naming_save_name}

#comparison of out of equilibrium and different values for mobility
gamma_mobility = ["GM2", "GM1", "M16_1_75e12", "GM025"]
gamma_mobility_naming = [r"\textbf{GM2}", r"\textbf{GM1}", r"\textbf{GM05}", r"\textbf{GM025}"]
gamma_mobility_save_name = ["gamma_mobility_Forces", "gamma_mobility_imbibition_subplots"]
gamma_mobility_dict = {"viewed": gamma_mobility, "naming": gamma_mobility_naming, "save_name": gamma_mobility_save_name}


#comparison of equilibrium and different values for mobility
equi_mobility = ["M2", "M1", "M05", "M025"]
equi_mobility_naming = [r"\textbf{M2}", r"\textbf{M1}", r"\textbf{M05}", r"\textbf{M025}"]
equi_mobility_save_name = ["equi_mobility_Forces", "equi_mobility_imbibition_subplots"]
equi_mobility_dict = {"viewed": equi_mobility, "naming": equi_mobility_naming, "save_name": equi_mobility_save_name}

# comparison for different Radii
bigR_comp = ["R3_Equi", "R4_Equi", "R6_Equi"]
bigR_naming = [r"\boldmath{$r=3nm$}", r"\boldmath{$r=4nm$}", r"\boldmath{$r=6nm$}"]
bigR_comp_save_name = ["bigR_comp_Forces", "bigR_comp_imbibition_subplots"]
bigR_comp_dict = {"viewed": bigR_comp, "naming": bigR_naming, "save_name": bigR_comp_save_name}

# comparison for out of equilibrium and different Contact angles
gamma_contactAngle = ["GM025", "GCA45", "GCA75"]
gamma_contactAngle_naming = [r"\textbf{GCA15}", r"\textbf{GCA45}", r"\textbf{GCA75}"]
gamma_contactAngle_save_name = ["gamma_contactAngle_Forces", "gamma_contactAngle_imbibition_subplots"]
gamma_contactAngle_dict = {"viewed": gamma_contactAngle, "naming": gamma_contactAngle_naming, "save_name": gamma_contactAngle_save_name}

# Equi CA15
equi_LW_comp = ["CA15"]
equi_LW_comp_naming =  [r"\textbf{\texttt{phaseFieldFoam}}"]
equi_LW_comp_save_name = ["Forces_equi_singlecomp", "LW_comp_imbibition_subplots"]
equi_LW_comp_dict = {"viewed": equi_LW_comp, "naming": equi_LW_comp_naming, "save_name": equi_LW_comp_save_name}

# Equi CA Study
equi_comp = ["CA15", "CA45", "CA75"]
equi_comp_naming = [r"\boldmath{$\theta_{e}=15^{\circ}$}", r"\boldmath{$\theta_{e}=45^{\circ}$}", r"\boldmath{$\theta_{e}=75^{\circ}$}"]
equi_comp_save_name = ["Forces_equi_CAcomp", "Equi_comp_imbibition_subplots"]
equi_comp_dict = {"viewed": equi_comp, "naming": equi_comp_naming, "save_name": equi_comp_save_name}

# Equi CA Study old Mobility
equi_M05_comp = ["M05CA15", "M05CA45", "M05CA75"]
equi_M05_comp_naming = [r"\boldmath{$\theta_{e}=15^{\circ}$}", r"\boldmath{$\theta_{e}=45^{\circ}$}", r"\boldmath{$\theta_{e}=75^{\circ}$}"]
equi_M05_comp_save_name = ["Forces_equi_CAcomp", "Equi_comp_imbibition_subplots"]
equi_M05_comp_dict = {"viewed": equi_M05_comp, "naming": equi_M05_comp_naming, "save_name": equi_M05_comp_save_name}

# pressure test
pressure_test = ["CA15"]
pressure_test_naming = [r"\textbf{\texttt{pressure}}"]
pressure_test_save_name = ["_", "LW_comp_imbibition_subplots"]
pressure_test_dict = {"viewed": pressure_test, "naming": pressure_test_naming, "save_name": pressure_test_save_name}

# Mesh comparison
mesh_comp = ["MeshCA15", "MeshDCA15"]
mesh_comp_naming = [r"\boldmath{$M1$}", r"\boldmath{$M2$}"]
mesh_comp_save_name = ["_", "Mesh_Comparison_imbibition_subplots"]
mesh_comp_dict = {"viewed": mesh_comp, "naming": mesh_comp_naming, "save_name": mesh_comp_save_name}


# choose the comparison you want to plot
data_sets = equi_LW_comp_dict
VIEWED_SIMULATIONS = data_sets["viewed"]
NAMING_SIMULATIONS = data_sets["naming"]
SAVE_NAME = data_sets["save_name"]

# Global path to the datasets!
# GLOBAL_PATH
#    |--- Simulation_1
#    |--- Simulation_2
#    |--- Simulation_xxx
#    |--- Plots
#
# A folder called Plots will be created in the data(GLOBAL_PATH) folder, if not already present.
GLOBAL_PATH = f"{script_directory}/data"

if __name__ == '__main__':
    analysis = Analysis(GLOBAL_PATH, VIEWED_SIMULATIONS, NAMING_SIMULATIONS)
    analysis.load_simulations()
    vis = analysis.postprocess()
    # to see availabe data, uncomment the following line
    #analysis.simulations[0].print_info()
    
    # plot generation 
    
    vis.subplot(xy=[["Time"], ["imbibition_height"]], fig_size=(14, 7), font_size=18, save=True, save_name=SAVE_NAME[1], show=True, n_th=1, x_limits=None, monocolor=True, start_from=2, lw=1)
