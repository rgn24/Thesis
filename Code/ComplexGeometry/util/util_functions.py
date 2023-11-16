import numpy as np

def wedify(z: np.array, angle) -> np.array:

        z_wedge = z * np.cos(np.deg2rad(angle / 2))
        y_wedge = z * np.sin(np.deg2rad(angle / 2))
        print(f"y: {y_wedge}, z: {z_wedge}")
        return y_wedge, z_wedge