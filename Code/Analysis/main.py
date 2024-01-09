import os

from util.Analysis import Analysis
GLOBAL_PATH = "M:\DataPlots_"

GLOBAL_PATH = "M:\FINAL_DATA"
#GLOBAL_PATH = "M:\Data_Plots\compMesh"
print(os.listdir(GLOBAL_PATH))

gamma_comp = ["CA15", "GM025"]
gamma_naming = [r"\textbf{Equi}", r"\textbf{Gamma}"]
gamma_naming_save_name = ["gammaComp_Forces", "gamma_Comp_imbibition_subplots"]
gamma_comp_dict = {"viewed": gamma_comp, "naming": gamma_naming, "save_name": gamma_naming_save_name}

gamma_study_comp = ["M16_1_0e13", "M16_2_0e12", "M16_1_75e12", "M16_1_5e12"]
gamma_study_naming = [r"\boldmath{$1.00\cdot 10^{13}$}", r"\boldmath{$2.00\cdot 10^{12}$}", r"\boldmath{$1.75\cdot 10^{12}$}", r"\boldmath{$1.50\cdot 10^{12}$}"]
gamma_study_naming_save_name = ["gammaStudy_Forces", "gamma_Study_imbibition_subplots"]
gamma_study_comp_dict = {"viewed": gamma_study_comp, "naming": gamma_study_naming, "save_name": gamma_study_naming_save_name}

gamma_mobility = ["GM2", "GM1", "M16_1_75e12", "GM025"]
gamma_mobility_naming = [r"\textbf{GM2}", r"\textbf{GM1}", r"\textbf{GM05}", r"\textbf{GM025}"]
gamma_mobility_save_name = ["gamma_mobility_Forces", "gamma_mobility_imbibition_subplots"]
gamma_mobility_dict = {"viewed": gamma_mobility, "naming": gamma_mobility_naming, "save_name": gamma_mobility_save_name}

equi_mobility = ["M2", "M1", "M05", "M025"]
equi_mobility_naming = [r"\textbf{M2}", r"\textbf{M1}", r"\textbf{M05}", r"\textbf{M025}"]
equi_mobility_save_name = ["equi_mobility_Forces", "equi_mobility_imbibition_subplots"]
equi_mobility_dict = {"viewed": equi_mobility, "naming": equi_mobility_naming, "save_name": equi_mobility_save_name}


bigR_comp = ["R3_Equi", "R4_Equi", "R6_Equi"]
bigR_naming = [r"\boldmath{$r=3nm$}", r"\boldmath{$r=4nm$}", r"\boldmath{$r=6nm$}"]
bigR_comp_save_name = ["bigR_comp_Forces", "bigR_comp_imbibition_subplots"]
bigR_comp_dict = {"viewed": bigR_comp, "naming": bigR_naming, "save_name": bigR_comp_save_name}

gamma_contactAngle = ["GM025", "GCA45", "GCA75"]
gamma_contactAngle_naming = [r"\textbf{GCA15}", r"\textbf{GCA45}", r"\textbf{GCA75}"]
gamma_contactAngle_save_name = ["gamma_contactAngle_Forces", "gamma_contactAngle_imbibition_subplots"]
gamma_contactAngle_dict = {"viewed": gamma_contactAngle, "naming": gamma_contactAngle_naming, "save_name": gamma_contactAngle_save_name}

equi_LW_comp = ["CA15"]
equi_LW_comp_naming =  [r"\textbf{\texttt{phaseFieldFoam}}"]
equi_LW_comp_save_name = ["Forces_equi_singlecomp", "LW_comp_imbibition_subplots"]
equi_LW_comp_dict = {"viewed": equi_LW_comp, "naming": equi_LW_comp_naming, "save_name": equi_LW_comp_save_name}

equi_comp = ["CA15", "CA45", "CA75"]
equi_comp_naming = [r"\boldmath{$\theta_{e}=15^{\circ}$}", r"\boldmath{$\theta_{e}=45^{\circ}$}", r"\boldmath{$\theta_{e}=75^{\circ}$}"]
equi_comp_save_name = ["Forces_equi_CAcomp", "Equi_comp_imbibition_subplots"]
equi_comp_dict = {"viewed": equi_comp, "naming": equi_comp_naming, "save_name": equi_comp_save_name}

equi_M05_comp = ["M05CA15", "M05CA45", "M05CA75"]
equi_M05_comp_naming = [r"\boldmath{$\theta_{e}=15^{\circ}$}", r"\boldmath{$\theta_{e}=45^{\circ}$}", r"\boldmath{$\theta_{e}=75^{\circ}$}"]
equi_M05_comp_save_name = ["Forces_equi_CAcomp", "Equi_comp_imbibition_subplots"]
equi_M05_comp_dict = {"viewed": equi_M05_comp, "naming": equi_M05_comp_naming, "save_name": equi_M05_comp_save_name}

pressure_test = ["CA15"]
pressure_test_naming = [r"\textbf{\texttt{pressure}}"]
pressure_test_save_name = ["_", "LW_comp_imbibition_subplots"]
pressure_test_dict = {"viewed": pressure_test, "naming": pressure_test_naming, "save_name": pressure_test_save_name}

mesh_comp = ["MeshCA15", "MeshDCA15"]
mesh_comp_naming = [r"\boldmath{$M1$}", r"\boldmath{$M2$}"]
mesh_comp_save_name = ["_", "Mesh_Comparison_imbibition_subplots"]
mesh_comp_dict = {"viewed": mesh_comp, "naming": mesh_comp_naming, "save_name": mesh_comp_save_name}

VIEWED_SIMULATIONS = equi_LW_comp_dict["viewed"]
NAMING_SIMULATIONS = equi_LW_comp_dict["naming"]
SAVE_NAME = equi_LW_comp_dict["save_name"]

if __name__ == '__main__':
    pass
    analysis = Analysis(GLOBAL_PATH, VIEWED_SIMULATIONS, NAMING_SIMULATIONS)
    analysis.load_simulations()
    vis = analysis.postprocess()
    #vis.plot(xy=[["Time"], ["f_p", "f_t", "f_w"]], log_log="semilogx", save=True, save_name=SAVE_NAME[0], show=True, n_th="log", y_limits=None, x_limits=[0,None], monocolor=True, linestyle="-", start_from=1)
    #vis.plot(xy=[["Time"], ["slope"]], log_log="semilogx", save=True, save_name="predicted_radius", show=True,
    #         n_th="log", y_limits=None, monocolor=True, linestyle="-")
    #vis.plot(xy=[["Time"], ["ca_first_element", "ca_radius", "ca_cox_voinov"]], log_log="semilogx", save=False, save_name=SAVE_NAME[0],
    #         show=True,
    #         n_th="log", y_limits=None, monocolor=True, linestyle="-")

    #vis.plot(xy=[["imbibition_height"], ["f_p_over_f_t"]], log_log=None, save=True, save_name=f"{SAVE_NAME[0]}_fp_ft_over_imbibition", show=True, n_th=10, y_limits=[0,None], monocolor=True)
    #vis.plot(xy=[["Time"], ["imbibition_height"]], log_log="loglog", save=False, save_name=SAVE_NAME[0], show=True, n_th=None, y_limits=None, monocolor=False, lw=1, start_from=2)
    #vis.plot(xy=[["Time"], ["slope"]], log_log=None, save=False, save_name=SAVE_NAME[0], show=True,
    #         n_th=None, y_limits=[0,2], monocolor=False,  start_from=2)
    vis.subplot(xy=[["Time"], ["imbibition_height"]], fig_size=(14, 7), font_size=14, log_log="loglog", save=True, save_name=SAVE_NAME[1], show=True, n_th=1, x_limits=None, monocolor=True, start_from=2, lw=1)
    #vis.subplot(xy=[["Time"], ["f_p_over_f_t"]], fig_size=(14, 7), font_size=14, log_log="loglog", save=True,
    #            save_name=SAVE_NAME[1]+"_fpft_over_time", show=True, n_th=20, y_limits=None, monocolor=False, active=True)
    #vis.plot(xy=[["Time"], ["ca_cox_voinov"]], log_log="semilogx", save=True, save_name=SAVE_NAME[0], show=True, n_th=10, y_limits=None, monocolor=True)
    #vis.plot(xy=[["Time"], ["slope"]], log_log="semilogx", save=True, save_name=SAVE_NAME[0], show=True, n_th=None, y_limits=None, monocolor=False)