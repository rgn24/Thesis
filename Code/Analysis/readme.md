Um die Analyse durchzuführen, müss zunächst definiert werden welche daten untersucht werden sollen. Dazu sind in ```main.py``` einige voreingestellte Vergleiche mit den jeweiligen daten in den Zeilen ```13``` bis ```78``` erstellt. 
Um zu definieren welcher Vergleich durhcgeführt wird, muss in Zeile ```82``` das dictionary gesetzt werden.
## Example
Eine Vergleich besteht immer aus 4 definitionen
```# Equi CA15
equi_LW_comp = ["CA15"] # Name of the folder in which the data is stored
equi_LW_comp_naming =  [r"\textbf{\texttt{phaseFieldFoam}}"] # Name in the plots (not mandatory)
equi_LW_comp_save_name = ["Forces_equi_singlecomp", "LW_comp_imbibition_subplots"] # Names of the wanted names to save plots (not mandatory)
equi_LW_comp_dict = {"viewed": equi_LW_comp, "naming": equi_LW_comp_naming, "save_name": equi_LW_comp_save_name} # wraping of the lists in a dict for later use
```
The dict is used to specify which comparison should be used. 
```# choose the comparison you want to plot
data_sets = equi_LW_comp_dict
VIEWED_SIMULATIONS = data_sets["viewed"]
NAMING_SIMULATIONS = data_sets["naming"]
SAVE_NAME = data_sets["save_name"]
```
Here the above shown dict is planed to be visualized. For that only line 82, needs to be changed. 
Um die Darstellung festzulegen, können einigen Einstellungen vorgenommen werden. Es gibt eine ```plot``` und eine ```subplot``` methode. Diese können die Selben einstellungen erhalten. Die ```subplot``` methode erstellt hierbei standardmäßig eine Variante in linaerer und eine in logarithmischer skallierung. Es ist möglich durch aktivierung der ```active``` bedingung dafür zu sorgen, dass der zweite plot im subplot die achsen vertauscht. 
Die möglichen einstellungen sind in den Docstrings dargestellt.