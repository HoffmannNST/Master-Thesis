#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import matplotlib.pyplot as plt

# FUNCTIONS    
# Calculate
def make_plot(r2_table, data_names, data, data_dae):
    X = r2_table.iloc[:, 0]

    # Plot Arrhenius r^2(p)
    fig1, axsrp = plt.subplots(2,2)
    fig1.suptitle('Arrhenius r^2(p)')
    axsrp[0,0].scatter(X, r2_table.iloc[:, 1])
    axsrp[0,0].set_title(data_names[0])
    try:
        axsrp[0,1].scatter(X, r2_table.iloc[:, 2])
        axsrp[0,1].set_title(data_names[1])
    except:
        pass
    try:
        axsrp[1,0].scatter(X, r2_table.iloc[:, 3])
        axsrp[1,0].set_title(data_names[2])
    except:
        pass
    try:
        axsrp[1,1].scatter(X, r2_table.iloc[:, 4])
        axsrp[1,1].set_title(data_names[3])
    except:
        pass

    for ax in axsrp.flat:
        ax.set(xlabel='p', ylabel='r^2')
    fig1.tight_layout()

    # Plot raw data R(T)
    fig2, axsRT = plt.subplots(2,2)
    fig2.suptitle('R(T)')
    x = -1
    for i in data_names:
        x += 1
        temp_data = data[x]
        if x == 0:
            axsRT[0,0].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 1])
            axsRT[0,0].set_title(i)

        if x == 1:
            axsRT[0,1].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 1])
            axsRT[0,1].set_title(i)
            
        if x == 2:
            axsRT[1,0].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 1])
            axsRT[1,0].set_title(i)
            
        if x == 3:
            axsRT[1,1].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 1])
            axsRT[1,1].set_title(i)

        for ax in axsRT.flat:
            ax.set(xlabel='T [Kelvin]', ylabel='R [Ohm]')
        fig2.tight_layout()

    # Plot DAE(T)
    fig3, axsDAE = plt.subplots(2,2)
    fig3.suptitle('DAE(T)')
    x = -1
    for i in data_names:
        x += 1
        temp_data = data_dae[x]
        if x == 0:
            axsDAE[0,0].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 5])
            axsDAE[0,0].set_title(i)

        if x == 1:
            axsDAE[0,1].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 5])
            axsDAE[0,1].set_title(i)
            
        if x == 2:
            axsDAE[1,0].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 5])
            axsDAE[1,0].set_title(i)
            
        if x == 3:
            axsDAE[1,1].scatter(temp_data.iloc[:, 0], temp_data.iloc[:, 5])
            axsDAE[1,1].set_title(i)

        for ax in axsDAE.flat:
            ax.set(xlabel='T [Kelvin]', ylabel='DAE [eV] (???)')
        fig3.tight_layout()

    plt.show()
    
    # ZMIENIĆ PLOTOWANIE NA UKŁADANIE WYKRESÓW PLIKAMI, A NIE TYPEM DANYCH !!!
