import pandas as pd
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self, simulations:list) -> None:
        self.simulations = simulations
        self.plot()
        
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
            print("VIZ ", simulation.df.head())