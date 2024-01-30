Since some simulations were conducted in different comparisons and are used later on, it is possible, that some names of simulations might not be the same as the other to compare. The gamma mobility case for example uses four simulations, in which one has a different name, but is the correct simulation. 

To perform the analysis, it is first necessary to define which data should be examined. For this, some predefined comparisons with the respective data are created in `main.py` from lines `8` to `73`. 
To define which comparison will be performed, the dictionary must be set in line `77`.

## Example

A comparison always consists of 4 definitions

```python
# Equi CA15
equi_LW_comp = ["CA15"] # Name of the folder in which the data is stored
equi_LW_comp_naming =  [r"\textbf{\texttt{phaseFieldFoam}}"] # Name in the plots (not mandatory)
equi_LW_comp_save_name = ["Forces_equi_singlecomp", "LW_comp_imbibition_subplots"] # Names of the wanted names to save plots (not mandatory)
equi_LW_comp_dict = {"viewed": equi_LW_comp, "naming": equi_LW_comp_naming, "save_name": equi_LW_comp_save_name} # Wrapping of the lists in a dict for later use
```

The dict is used to specify which comparison should be used, as mentioned before. 
```python
# choose the comparison you want to plot
data_sets = equi_LW_comp_dict
VIEWED_SIMULATIONS = data_sets["viewed"]
NAMING_SIMULATIONS = data_sets["naming"]
SAVE_NAME = data_sets["save_name"]
```

Here the above shown dict is planned to be visualized. For that, only line ```77``` needs to be changed.

To see, which data can be used to plot insert 
```python 
analysis.simulations[0].print_info()
```
to your code. Then you will get some basic info about the first simulation in your viewed simulations. The keywords in the output "cols" are the ones you need to use, to plot the data. 

To define the presentation, some settings can be made. There is a ```plot``` and a ```subplot``` method. These can receive the same settings. The ```subplot``` method by default creates one variant in linear and one in logarithmic scaling. It is possible to ensure that the second plot in the subplot swaps the axes by activating the active condition.

The possible settings are displayed in the docstrings.