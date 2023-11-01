import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['text.usetex'] = True

class Visualization:
    def __init__(self, simulations:list, dump_path="") -> None:
        self.simulations = simulations
        self.dump_path = dump_path + "/Plots"
        
    def set_color(self):
        COLOR_TEMPLATE = [
            "#D32F2F",  # Rot
            "#1976D2",  # Blau
            "#388E3C",  # Grün
            "#FBC02D",  # Gelb
            "#8E24AA",  # Lila
            "#D84315",  # Orange
            "#0288D1",  # Himmelblau
            "#7B1FA2",  # Dunkellila
            "#C2185B",  # Pink
            "#7E57C2",  # Indigo
            "#0288D1",  # Hellblau
            "#5D4037"   # Braun
        ]
        
    def plot(self):
        for simulation in self.simulations:
            x = xy[0][0]
            for id_y, y in enumerate(xy[1]):
                #TODO refactor
                if len(xy[1]) > 1:
                    label_name = simulation.name + " " + y
                else:
                    label_name = simulation.name
                    
                dx = simulation.df[x]
                dy = simulation.df[y]
                if n_th is not None and n_th == "log":
                    dx = self.get_log_elems(dx)
                    dy = self.get_log_elems(dy)
                ax.plot(dx[::spacing_plot], dy[::spacing_plot], label=label_name, marker="o", linestyle="None")
            
        # plot settings
        if log_log =="loglog":
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
        plt.grid()
        
        
        if save:
            if save_path == "":
                print(xy[1][0])
                name_y = ""
                for substr in xy[1]: name_y += substr + "_"
                plt.savefig(self.dump_path + xy[0][0] + "_over_" + name_y +".pdf", bbox_inches='tight')
            else:
                plt.savefig(save_path + ".pdf", bbox_inches='tight')
        if show:
            plt.show()