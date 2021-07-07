#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

# FUNCTIONS    
# Calculate
def make_plot(data, data_names, data_dae, r2_table):
    """Function that makes plots of 3 different functions and saves them as .png files.

    Args:
        data (list): list of DataFrames of raw data
        data_names (list): list of names of files imported to program
        data_dae (list): list of DataFrames of calculted data
        r2_table (pandas.DataFrame): table of r^2 (cube of pearson coeficient) values
    """
    pathlib.Path('Results/Plots').mkdir(parents=True, exist_ok=True)

    # Plot r^2(p)
    X = r2_table.iloc[:, 0]
    for count, item in enumerate(data_names, 1):
        Y = r2_table.iloc[:,count]
        plt.xlabel('p')
        plt.ylabel('r$^{2}$')
        plt.title(item, {'horizontalalignment': 'center'})
        plt.suptitle('Arrhenius r$^{2}$(p)')
        plt.scatter(X,Y) 
        file_path = 'Results/Plots/r2_' + item + '.png'
        plt.savefig(file_path, dpi=300)
        #plt.show()
        plt.close()

    # Plot raw data R(T)
    for count, item in enumerate(data_names, 0):
        temporary_data = data[count]
        X = temporary_data.iloc[:, 0]
        Y = temporary_data.iloc[:, 1]
        plt.xlabel('T [Kelvin]')
        plt.ylabel('R [Ohm]')
        plt.title(item, {'horizontalalignment': 'center'})
        plt.suptitle('R(T)')
        plt.scatter(X,Y) 
        file_path = 'Results/Plots/RT_' + item + '.png'
        plt.savefig(file_path, dpi=300)
        #plt.show()
        plt.close()

    # Plot DAE(T)
    for count, item in enumerate(data_names, 0):
        temporary_data = data_dae[count]
        X = temporary_data.iloc[:, 0]
        Y = temporary_data.iloc[:, 5]
        plt.xlabel('T [Kelvin]')
        plt.ylabel('DAE [eV]')
        plt.title(item, {'horizontalalignment': 'center'})
        plt.suptitle('DAE(T)')
        plt.scatter(X,Y) 
        file_path = 'Results/Plots/DAE_' + item + '.png'
        plt.savefig(file_path, dpi=300)
        #plt.show()
        plt.close()
        
