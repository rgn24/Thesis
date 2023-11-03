import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['text.usetex'] = True

class Visualization:
    def __init__(self, simulations:list, dump_path="") -> None:
        self.simulations = simulations
        self.dump_path = dump_path + "/Plots"
        
    def set_color(self):
        pass
    
    def get_log_elems(self, data_set):
        i = 0
        i_c = 0
        ret_arr = []
        for id_e, elem in enumerate(data_set):
            if (id_e+1) % 10**i == 0:
                if i_c==10:
                    i+=1
                    i_c = 1
                    continue
                ret_arr.append(elem)
                i_c+=1
        return ret_arr
    
    def get_naming(self, arg:list) -> str:
        naming_dict = {"Time": r"Time in $s$", 
                       "max(CACoordsX)": r"position of meniscus valley in $m$", 
                       "velocity": r"velocity magnitude in $m/s$", 
                       "imbibition_height": r"imbibition height in $m$", 
                       "radius": r"computed radius in $m$", 
                       "ca_radius": r"computed radius with the contact angle in $m$", 
                       "ca_first_element": r"dynamic contact angle $\theta_\mathrm{D}$", 
                       "radius_pressure": r"computed radius with pressure difference in $m$", 
                       "predicted_pressure": r"predicted pressure in $Pa$", 
                       "pressure_error": r"error of pressure prediction", 
                       "PD": r"pressure difference in $Pa$",
                       "f_p": r"Poseuille Forces in $N$",
                       "f_t": r"Total viscous forces in $N$", 
                       "f_w": r"Wedge forces in $N$",}
        ret_str = ""
        for id_e, elem in enumerate(arg):
            if len(arg) > 1 and id_e != len(arg)-1:
                str_name = naming_dict[elem]+", "
                ret_str+= str_name
            else:
                ret_str+=naming_dict[elem]
        return ret_str
    
    def lucas_washburn(self, t, theta=None):
        r=3e-9
        sigma = 0.072
        eta = 2e-6
        #print(theta)
        theta = np.deg2rad(theta)
        #print(theta)
        if theta is None:
            theta = float(15)
        lw = np.sqrt((r*sigma * np.cos(theta)/(2*eta)) * t)
        lw[0] = np.nan
        return 0.042*lw
        
    def plot(self, xy:list=[[],[]], font_size:int=12, log_log=None, show:bool = True, save:bool = False, save_path:str = "", xy_name:list=None, x_limits:list=None, y_limits:list=None, n_th=None): 
        # checks if the input is valid
        if n_th == "log":
            spacing_plot = 1
        else:
            spacing_plot = n_th
        
        
        fig, ax = plt.subplots(figsize=(12, 8))
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
                ax.plot(dx[::spacing_plot], dy[::spacing_plot], label=label_name, marker=".", linestyle="None")
            
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