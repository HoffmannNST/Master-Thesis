#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import numpy as np
from math import exp
from scipy import stats, constants

# Predefined settings
data = []
data_dae = []

# FUNCTIONS    
# Calculate Arrhenius
def calculate_arrhenius(data, data_names):
    x = -1

    try:
        #p_step = float(input('\nEnter the step for the p parameter (i.e. 0.1): '))
        p_step = 0.1
    except:
        print('Invalid input!')
        p_step = 0.1

    p_list = []
    for p in np.arange(0+p_step, 1+p_step, p_step):
        p_list.append(round(p,3))

    # Tables of calculated parameters
    r2_table = pd.DataFrame(p_list, columns = ['p'])    # r2 is a correlation coeaficient
    T0_table = pd.DataFrame(p_list, columns = ['p'])    # T0 is a characteristic temp. deriviated from slope of function
    R0_table = pd.DataFrame(p_list, columns = ['p'])    # R0 is a pre-exponential factor deriviated from intercept of function

    for i in data_names:
        x += 1

        temp_data = data[x]
        new_data = temp_data.loc[:,['Temperatura [K]', 'Opor']]
        new_data['Ln(1/R)'] = np.log(1/new_data['Opor'])
        
        Y = new_data['Ln(1/R)']
        r2_list = []
        T0_list = []
        R0_list = []

        for p in np.arange(0+p_step, 1+p_step, p_step):
            column_p_name = '1/T^(' + str(round(p,3)) + ')'
            new_data[column_p_name] = 1/(new_data['Temperatura [K]']**p)
            X = new_data[column_p_name]
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
            del p_value
            del std_err
            r2_list.append(r_value**2)
            slope *= -1
            T0_list.append(slope**(1/p))
            R0_list.append(exp(-intercept))

        r2_table[i] = r2_list
        T0_table[i] = T0_list
        R0_table[i] = R0_list
        data[x] = new_data

    #print('\nCalculated r^2(p):\n', r2_table)
    #print('\nCalculated T0 parameter:\n', T0_table)
    #print('\nCalculated R0 parameter:\n', R0_table)

    print('\nMax values of r^2(p):')
    for i,j in enumerate(data_names):
        index_p = r2_table[j].idxmax()
        max_r2 = r2_table.iloc[index_p,i+1]
        param_p = r2_table.iloc[index_p,0]
        param_T0 = T0_table.iloc[index_p,i+1]
        param_R0 = R0_table.iloc[index_p,i+1]
        print('%s. max r^2 = %.3f for p = %.2f, parameters T0 = %.2f, R0 = %.2f, for data %s' % (i+1,max_r2,param_p,param_T0,param_R0,j))

    return data, r2_table

# Calculate Differential Activation Energy
def calculate_dae(data, data_names):
    data_dae = data
    Kb = constants.value("Boltzmann constant in eV/K") # "Boltzmann constant" or "...in eV/K" or "...in Hz/K" or "...in inverse meter per kelvin"

    x = -1
    for i in data_names:
        x += 1

        temp_data = data_dae[x]
        new_data = temp_data.loc[:,['Temperatura [K]', 'Opor']]
        #new_data['Ln(R)'] = np.log(new_data['Opor'])
        new_data['d(Ln(R))'] = (np.log(new_data['Opor'])).diff()
        #new_data['(Kb*T)^(-1)'] = (new_data['Temperatura [K]']*Kb)
        new_data['d(Kb*T)^(-1)'] = (new_data['Temperatura [K]']*Kb).diff()
        new_data['DAE'] = new_data['d(Ln(R))']/new_data['d(Kb*T)^(-1)'] # ?????? Możliwe, ze można w jednej linijce, ale nwm czy nie lepiej zostawić kilka kolumn w DataFrame dla kontroli
        
        print("\n",i)
        print(new_data)
        data_dae[x] = new_data 
