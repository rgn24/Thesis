import numpy as np


class DataFrameUtilityMixin:
    def compute_velocity(self):
        u = [np.nan]
        for index, row in self.iterrows():
            if index == 0:
                row_prev = row
                continue
            u.append((row["imbibition_height"] - row_prev["imbibition_height"]) / (row["Time"] - row_prev["Time"]))
            row_prev = row
        self["velocity"] = u

    def compute_imbibition_height(self, height: float):
        """Computes the imbibition Height of the Meniscus in the capillary. The Meniscus Position is is used as the the position on the axis of the capillary.

        Args:
            height (float): Height of the capillary
        """
        self["imbibition_height"] = height - self["max(coordsX_Meniscus)"]

    def compute_radius(self, capillary_radius: float = 3e-9):
        """Computes the Radius of the Meniscus with the known Radius of the Capillary.

        Args:
            capillary_radius (float): Radius of the Capillary
        """
        h = self["max(coordsX_Meniscus)"] - self["min(coordsX_Meniscus)"]
        # FIXME: not working somehow; Radius is not defined in dataframe after computation...
        self["radius"] = capillary_radius ** 2 / (2 * h) + h

    def compute_ca_radius(self):
        """Computes the Contact Angle using the computed radius of the meniscus
        """
        h = h = self["max(coordsX_Meniscus)"] - self["min(coordsX_Meniscus)"]
        self["ca_radius"] = 90 - 2 * np.rad2deg(np.arctan(h / self["radius"]))

    def compute_ca_first_Element(self, h_first_element: float = 0.3e-9):
        """Compute the Contact angle using only the first element of the capillary. Technically every distance of the measured height is possible here.

        Args:
            h_first_element (float): Height of the first element of the capillary from the wall. Could be a value in between two elements as well.
        """
        # TODO check, if can be computed. If not, set to NaN
        h = self["max(CACoordsX)"] - self["min(CACoordsX)"]
        self["ca_first_element"] = np.rad2deg(np.arctan(h_first_element / h))

    def compute_slope(self):
        """Computes the slope of the Meniscus
        """
        slope = [np.nan]
        for index, row in self.iterrows():
            if index == 0:
                row_prev = row
                continue
            if row["imbibition_height"] < 0:
                slope.append(np.nan)
                row_prev = row
                continue
            slope.append(np.log((row["imbibition_height"] / row_prev["imbibition_height"])) / np.log((row["Time"] / row_prev["Time"])))
            row_prev = row
        self["slope"] = slope


    def compute_pressure_difference(self):
        """Computes the Pressure Difference between the Meniscus and the Capillary
        """

        self["PD"] = self["max(Result)"] - self["min(Result)"]

    def compute_radius_pressure(self):
        """Computes the predicted radius from the pressure drop of measured in the Simulation.
        """
        sigma = 0.072
        self["radius_pressure"] = 2 * sigma / self["PD"]

    def compute_predicted_pressure(self):
        """Computes the predicted pressure from the radius of the meniscus computed with simulation data
        """
        sigma = 0.072
        self["predicted_pressure"] = 2 * sigma / self["radius"]

    def compute_pressure_error(self):
        """Computes the ratio of the predicted Pressure and the Pressure Drop measured in the Simulation.
        """
        # TODO check, if used right in the paper
        self["pressure_error"] = (1-(self["PD"] / self["predicted_pressure"]))*100



    def compute_poiseuille_forces(self):
        mu = 1e-3
        self["f_p"] = 8 * np.pi * self["velocity"] * mu * self["imbibition_height"]

    def compute_total_visc_force(self):
        # print(self.columns)
        total_visc_f = []
        for index, row in self.iterrows():
            try:
                temp = float(row["divDevRhoTot(N)"].strip("(").split(" ")[0]) * 72  # 360/5
            except:
                temp = np.nan
            total_visc_f.append(temp)
        self["f_t"] = total_visc_f

    def compute_wedge_forces(self):
        self["f_w"] = self["f_t"] - self["f_p"]

    def compute_vis_drag_over_total_visc(self):
        self["f_p_over_f_t"] = self["f_p"] / self["f_t"]

    def compute_cox_voinov_angle(self, theta_e: float):
        """Computes the contact angle using the Cox-Voinov Equation. Using the Velocity of the Meniscus from the Simulation data and a given equilibrium contact angle

        Args:
            theta_e (float): Equilibrium contact angle
        """
        mu = 1e-3
        sigma = 0.072
        ca = self["velocity"] * mu / sigma
        ln_l = np.log(3000 / 1)#np.log(160 / 1)
        self["ca_cox_voinov"] = np.rad2deg(np.power(np.power(np.deg2rad(theta_e), 3) + 9 * ca * ln_l, 1 / 3))

    def compute_ruiz(self, theta_e=15):
        mu = 1e-3
        sigma = 0.072
        r = 3e-9
        fm_ruiz = [np.nan]
        for index, row in self.iterrows():
            if index == 0:
                continue

            # fm_ruiz.append(2 * np.pi * r * sigma * (np.cos(np.deg2rad(theta_e)) - np.cos(np.deg2rad(row["CA_CA_FE"]))))
            fm_ruiz.append(
                2 * np.pi * r * sigma * (np.cos(np.deg2rad(theta_e)) - np.cos(np.deg2rad(row["ca_cox_voinov"]))))
            # fm_ruiz.append(2 * np.pi * r * sigma * (np.cos(np.deg2rad(theta_e)) - np.cos(np.deg2rad(row["contactAngle"]))))
        # print(fm_ruiz)
        self["fm_ruiz"] = fm_ruiz

