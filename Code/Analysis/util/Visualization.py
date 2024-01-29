import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pylab import *
from typing import Optional

plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')
plt.rcParams['text.latex.preamble'] = r'\usepackage{lmodern}'

class Visualization:
    def __init__(self, simulations: list, dump_path="", longest_id: int = 0) -> None:
        self.simulations = simulations
        self.dump_path = dump_path + "/Plots/"
        self.longest = longest_id


        # dictionary to get better looking visuals of the plots for the supported quantities
        self.naming_dict = {"Time": [r"Time", r" in $s$"],
                            "max(CACoordsX)": [r"position of meniscus valley", r" in $m$"],
                            "velocity": [r"velocity magnitude", r" in $m/s$"],
                            "imbibition_height": [r"imbibition height", r" in $m$"],
                            "radius": [r"computed radius", r" in $m$"],
                            "ca_radius": [r" contact angle computed with radius", r""],
                            "ca_first_element": [r"first Element contact angle", r""],
                            "radius_pressure": [r"computed radius with pressure difference", r" in $m$"],
                            "predicted_pressure": [r"predicted pressure", r" in $Pa$"],
                            "pressure_error": [r"error of pressure prediction", r""],
                            "PD": [r"pressure difference from simulation", r" in $Pa$"],
                            "f_p": [r"Poseuille Forces", r" in $N$"],
                            "f_t": [r"Total viscous forces", r" in $N$"],
                            "f_w": [r"meniscus resistance forces", r" in $N$"],
                            "fm_ruiz": [r"Ruiz prediction", r" in $N$"],
                            "f_p_over_f_t": [r"Poseuille Forces/Total viscous forces", r""],
                            "ca_cox_voinov": [r"Cox-Voinov contact angle", r""],
                            "slope": [r"Slope of the imbibition height", r""],}

    def set_style(self, monocolor: bool = False, len_y_sim: int = 1):
        """Set Style of plot. Namely color and Markers. If monocolor is set to True, the color for each simulation will be the same, no matter, if several quantities are plottet at the same time. Good for comparison of Simulations with other settings.
        In that case all the marker will be the same for different simualtions, but same quantities. 15 different markers are available.

        Args:
            monocolor (bool, optional): Value to decide, if the colr for one simulation will be the same. Defaults to False.
            len_y_sim (int, optional): number of simulaitons. Defaults to 1.

        Returns:
            _type_: color and marker settings for the plot
        """
        markers = [".", "v", "s", "+", "x", "^", "<", ">", "D", "p", "P", "*", "h", "H", "o"]
        if monocolor:
            n_colors = len(self.simulations)
        else:
            n_colors = len(self.simulations) * len_y_sim
        COLOR_MAP = plt.cm.get_cmap('Set1', n_colors)
        ret_arr_color = []
        ret_arr_marker = []
        n_plots = len(self.simulations) * len_y_sim
        if monocolor:
            c_color = 0
            for i in range(1, n_plots + 1):
                ret_arr_color.append(COLOR_MAP(c_color))
                ret_arr_marker.append(markers[i - 1 - c_color * len_y_sim])
                if i % len_y_sim == 0 and i != 0:
                    c_color += 1
        else:
            for i in range(n_plots):
                ret_arr_color.append(COLOR_MAP(i))
                ret_arr_marker.append(markers[i])
        return ret_arr_color, ret_arr_marker

    def get_log_elems(self, data_set):
        """filter the data set to get only every log_10th element. This is used for loglog plots, to get a better overview.

        Args:
            data_set (_type_): manipulated data set

        Returns:
            _type_: manipulated data set with only every log_10th element
        """
        i = 0
        i_c = 0
        ret_arr = []
        for id_e, elem in enumerate(data_set):
            if (id_e + 1) % 10 ** i == 0:
                if i_c == 10:
                    i += 1
                    i_c = 1
                    continue
                ret_arr.append(elem)
                i_c += 1
        return ret_arr

    def get_label(self, label_y: str = "", len_xy: int = 1, sim: object = None) -> str:
        """the the Name of the label for the plot. If more than one quantity is plotted, the name of the simulation will be added to the label.

        Args:
            label_y (str, optional): plotted quantity. Defaults to "".
            len_xy (int, optional): number of visualisied quantities. Defaults to 1.
            sim (object, optional): util.Simulation Object to get info about the simulation data. Defaults to None.

        Returns:
            str: label of the dataseries
        """
        if len_xy > 1:
            label_name = sim.name_plot + " " + self.naming_dict[label_y][0]
        else:
            label_name = sim.name_plot #+ " " + self.naming_dict[label_y][0]
        return label_name

    def get_naming(self, arg: list) -> str:
        ret_str_axis = ""
        for id_e, elem in enumerate(arg):
            if len(arg) > 1 and id_e != len(arg) - 1:
                str_name = self.naming_dict[elem][0] + self.naming_dict[elem][1] + ", "
                ret_str_axis += str_name
            else:
                ret_str_axis += self.naming_dict[elem][0] + self.naming_dict[elem][1]
        return ret_str_axis

    def lucas_washburn(self, t, theta=None):
        # TODO radius is as of now not variable. Should be changed
        r = 3e-9
        sigma = 0.072
        eta = 2e-6
        theta = np.deg2rad(theta)
        lw = np.sqrt((r * sigma * np.cos(theta) / (2 * eta)) * t)
        lw[0] = np.nan
        return 0.042 * lw

    def linear_growth(self, t, theta=None):
        r = 3e-9
        sigma = 0.072
        eta = 2e-6
        theta = np.deg2rad(theta)
        linear = 3*t
        linear[0] = np.nan
        return linear

    def get_diff_arr(self, arr1, arr2):
        return np.abs(arr1 - arr2)

    def plot(self, xy: list = [[], []], font_size: int = 12, fig_size: Optional[tuple] = (14, 8),
             log_log: Optional[str] = None, show: bool = True, save: bool = False, save_name: str = "",
             xy_name: Optional[list] = None, x_limits: Optional[list] = None, y_limits: Optional[list] = None,
             secondary_y: Optional[int] = None, n_th=None, monocolor: bool = False, lw: Optional[float] = None, linestyle="None", start_from:int=0):
        # checks if the input is valid
        """Plot of the provided list of simulations.

        Args:
            xy (list, optional): list with the x, y datasets to plot. Defaults to [[],[]].
            font_size (int, optional): font size of the texts in the plot. Defaults to 12.
            log_log (Optional[str], optional): logarithmic scaling of both or a single axis. Supported values are: "loglog", "semilogx", "semilogy" or None . Defaults to None.
            show (bool, optional): show the plot in runtime. Defaults to True.
            save (bool, optional): Save the plot. Defaults to False.
            save_path (str, optional): Path to save the plot. Defaults to "$SIM_DIR$/Plots/".
            xy_name (Optional[list], optional): Names of the axis. Defaults to provided quantities.
            x_limits (Optional[list], optional): Limits of the x-axis (lower, upper). Defaults to None.
            y_limits (Optional[list], optional): Limits of the y-axis (lower, upper). Defaults to None.
            secondary_y (Optional[int], optional): quantity, which should be plotted on the secondary y-axis. Defaults to None.
            n_th (_type_, optional): filter the data to each n_th-Element. Accepts integers or "log". Defaults to 1.
            monocolor (bool, optional): show each simulation data with one color to compare with other simulation. Defaults to False.
        """
        if n_th == "log":
            spacing_plot = 1
        else:
            spacing_plot = n_th

        fig = plt.figure(figsize=fig_size)
        ax = fig.add_subplot(111)
        ####

        ####

        color_map, marker_map = self.set_style(monocolor=monocolor, len_y_sim=len(xy[1]))
        style_id = 0
        for simulation in self.simulations:
            x = xy[0][0]
            for id_y, y in enumerate(xy[1]):
                dx = simulation.df[x]
                dy = simulation.df[y]
                if n_th is not None and n_th == "log":
                    dx = self.get_log_elems(dx)
                    dy = self.get_log_elems(dy)
                ax.plot(dx[start_from::spacing_plot], dy[start_from::spacing_plot], label=self.get_label(y, len(xy[1]), simulation),
                        marker=marker_map[style_id], linestyle=linestyle, color=color_map[style_id])
                style_id += 1

        ## plotting LW, if wanted
        if lw is not None:
            #print("LONGEST", self.longest, "Name", self.simulations[self.longest].name, "shape",
            #      self.simulations[self.longest].df["Time"].shape)
            lw_data = self.lucas_washburn(self.simulations[self.longest].df["Time"], lw)
            linear_data = self.linear_growth(self.simulations[self.longest].df[x], lw)
            # lw_data = lucas_washburn(t=datasets[longest_id].data[x])
            #print(len(lw_data))
            plt.plot(self.simulations[self.longest].df[x], lw_data, "-", color="black", label=r"\textbf{Lucas-Washburn}-prediction")
            if log_log == "loglog":
                plt.plot(self.simulations[self.longest].df[x], linear_data, "-", color="black", label=r"\textbf{$z\sim t$}", linestyle="dashed")


        # plot settings
        if log_log == "loglog":
            plt.loglog()
        elif log_log == "semilogx":
            plt.semilogx()
        elif log_log == "semilogy":
            plt.semilogy()
        elif log_log is None:
            pass
        else:
            print("input unknown valid inputs are: loglog, semilogx, semilogy or no input. Not scaling was applied")

        if xy_name is not None:
            ax.set_xlabel(xy_name[0], fontsize=font_size)
            ax.set_ylabel(xy_name[1], fontsize=font_size)
        else:
            ax.set_xlabel(self.get_naming(xy[0]), fontsize=font_size)
            ax.set_ylabel(self.get_naming(xy[1]), fontsize=font_size)
        if x_limits is not None:
            ax.set_xlim(x_limits)
        if y_limits is not None:
            ax.set_ylim(y_limits)
        ax.xaxis.get_offset_text().set_fontsize(font_size)
        ax.yaxis.get_offset_text().set_fontsize(font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        plt.legend(fontsize=font_size)
        plt.grid(which='both', linestyle='-', linewidth=0.7)
        plt.grid(which='minor', linestyle='--', linewidth=0.5)

        if save:
            if save_name == "":
                name_y = ""
                for substr in xy[1]: name_y += substr + "_"
                plt.savefig(self.dump_path + xy[0][0] + "_over_" + name_y + ".pdf", bbox_inches='tight')
                plt.savefig(self.dump_path + xy[0][0] + "_over_" + name_y + ".svg", bbox_inches='tight')
                print("saved at: ", self.dump_path + xy[0][0] + "_over_" + name_y + ".pdf")
            else:
                plt.savefig(self.dump_path + save_name + ".pdf", bbox_inches='tight')
                plt.savefig(self.dump_path + save_name + ".svg", bbox_inches='tight')
        if show:
            plt.show()

    def subplot(self, xy: list = [[], []], font_size: int = 12, fig_size: Optional[tuple] = (14, 8),
                log_log: Optional[str] = None, show: bool = True, save: bool = False, save_name: str = "",
                xy_name: Optional[list] = None, x_limits: Optional[list] = None, y_limits: Optional[list] = None,
                secondary_y: Optional[int] = None, n_th=None, monocolor: bool = False, lw: Optional[float] = None,
                longest_id: int = 0, start_from:int=0, active:bool=False):
        # checks if the input is valid
        """Plot of the provided list of simulations.

        Args:
            xy (list, optional): _description_. Defaults to [[],[]].
            font_size (int, optional): _description_. Defaults to 12.
            log_log (Optional[str], optional): logarithmic scaling of both or a single axis. Supported values are: "loglog", "semilogx", "semilogy" or None . Defaults to None.
            show (bool, optional): show the plot in runtime. Defaults to True.
            save (bool, optional): Save the plot. Defaults to False.
            save_path (str, optional): Path to save the plot. Defaults to "$SIM_DIR$/Plots/".
            xy_name (Optional[list], optional): Names of the axis. Defaults to provided quantities.
            x_limits (Optional[list], optional): Limits of the x-axis (lower, upper). Defaults to None.
            y_limits (Optional[list], optional): Limits of the y-axis (lower, upper). Defaults to None.
            secondary_y (Optional[int], optional): quantity, which should be plotted on the secondary y-axis. Defaults to None.
            n_th (_type_, optional): filter the data to each n_th-Element. Accepts integers or "log". Defaults to 1.
            monocolor (bool, optional): show each simulation data with one color to compare with other simulation. Defaults to False.
        """
        if n_th == "log":
            spacing_plot = 1
        else:
            spacing_plot = n_th

        fig, (ax1, ax2) = plt.subplots(figsize=fig_size, nrows=1, ncols=2)
        # ax = fig.add_subplot(111)
        ####

        color_map, marker_map = self.set_style(monocolor=monocolor, len_y_sim=len(xy[1]))
        style_id = 0

        # hardcoded change of second subplot to fpft over time. in the active case!!
        active = active



        for simulation in self.simulations:
            x = xy[0][0]
            for id_y, y in enumerate(xy[1]):
                if active:
                    dx2 = simulation.df["imbibition_height"]
                    dy2 = simulation.df["f_p_over_f_t"]
                    y2 = "f_p_over_f_t"
                else:
                    dx2 = simulation.df[x]
                    dy2 = simulation.df[y]
                    y2 = y
                dx = simulation.df[x]
                dy = simulation.df[y]
                if n_th is not None and n_th == "log":
                    dx = self.get_log_elems(dx)
                    dy = self.get_log_elems(dy)
                    dx2 = self.get_log_elems(dx)
                    dy2 = self.get_log_elems(dy)


                ax1.plot(dx[start_from::spacing_plot], dy[start_from::spacing_plot], label=self.get_label(y, len(xy[1]), simulation),
                         marker=marker_map[style_id], linestyle="None", color=color_map[style_id])
                ax2.plot(dx2[start_from::spacing_plot], dy2[start_from::spacing_plot], label=self.get_label(y2, len(xy[1]), simulation),
                         marker=marker_map[style_id], linestyle="None", color=color_map[style_id])
                style_id += 1

        ## plotting LW, if wanted
        if lw is not None:
            lw_data = self.lucas_washburn(self.simulations[self.longest].df[x], lw)
            linear_data = self.linear_growth(self.simulations[self.longest].df[x], lw)
            # lw_data = lucas_washburn(t=datasets[longest_id].data[x])
            ax1.plot(self.simulations[self.longest].df[x], lw_data, "-", color="black", label=r"\textbf{Lucas-Washburn}-prediction")
            if not active:
                ax2.plot(self.simulations[self.longest].df[x], lw_data, "-", color="black", label=r"\textbf{Lucas-Washburn}-prediction")
                ax2.plot(self.simulations[self.longest].df[x], linear_data, "-", color="black",
                     label=r"\textbf{$z\sim t$}", linestyle="dashed")
        if not active:
            ax2.loglog()

        # plot settings
        ##if log_log =="loglog":
        ##    plt.loglog()
        ##elif log_log == "semilogx":
        ##    plt.semilogx()
        ##elif log_log == "semilogy":
        ##    plt.semilogy()
        ##elif log_log is None:
        ##    pass
        ##else:
        ##    print("input unknown valid inputs are: loglog, semilogx, semilogy or no input. Not scaling was applied")

        if xy_name is not None:
            ax1.set_xlabel(xy_name[0], fontsize=font_size)
            ax1.set_ylabel(xy_name[1], fontsize=font_size)
            ax2.set_xlabel(xy_name[0], fontsize=font_size)
            ax2.set_ylabel(xy_name[1], fontsize=font_size)
        else:
            ax1.set_xlabel(self.get_naming(xy[0]), fontsize=font_size)
            ax1.set_ylabel(self.get_naming(xy[1]), fontsize=font_size)
            ax2.set_xlabel(self.get_naming(xy[0]), fontsize=font_size)
            ax2.set_ylabel(self.get_naming(xy[1]), fontsize=font_size)
            if active:
                ax2.set_xlabel(self.get_naming(["imbibition_height"]), fontsize=font_size)
                ax2.set_ylabel(self.get_naming(["f_p_over_f_t"]), fontsize=font_size)
        if x_limits is not None:
            ax1.set_xlim(x_limits)
            ax2.set_xlim(x_limits)
        if y_limits is not None:
            ax1.set_ylim(y_limits)
            ax2.set_ylim(y_limits)
        ax1.xaxis.get_offset_text().set_fontsize(font_size)
        ax1.yaxis.get_offset_text().set_fontsize(font_size)
        ax2.xaxis.get_offset_text().set_fontsize(font_size)
        ax2.yaxis.get_offset_text().set_fontsize(font_size)
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax1.legend(fontsize=font_size)
        ax2.legend(fontsize=font_size)
        ax1.grid(which='both', linestyle='-', linewidth=0.7)
        ax1.grid(which='minor', linestyle='--', linewidth=0.5)
        ax2.grid(which='both', linestyle='-', linewidth=0.7)
        ax2.grid(which='minor', linestyle='--', linewidth=0.5)

        if save:
            if save_name == "":
                name_y = ""
                for substr in xy[1]: name_y += substr + "_"
                plt.savefig(self.dump_path + xy[0][0] + "_over_" + name_y + ".pdf", bbox_inches='tight')
                plt.savefig(self.dump_path + xy[0][0] + "_over_" + name_y + ".svg", bbox_inches='tight')
                print("saved at: ", self.dump_path + xy[0][0] + "_over_" + name_y + ".pdf")
            else:
                plt.savefig(self.dump_path + save_name + ".pdf", bbox_inches='tight')
                plt.savefig(self.dump_path + save_name + ".svg", bbox_inches='tight')
        if show:
            plt.show()