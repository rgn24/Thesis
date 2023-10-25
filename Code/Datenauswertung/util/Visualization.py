import pandas as pd
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, simulations:list) -> None:
        self.simulations = simulations
        self.plot()
        
    def set_color(self):
        pass
        
    def plot(self):
        for simulation in self.simulations:
            print("VIZ ", simulation.df.head())