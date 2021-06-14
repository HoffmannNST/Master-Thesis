#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import numpy as np
from math import exp
from scipy import stats, constants

# Predefined settings
data = []
data_arr = []
data_dae = []

# FUNCTIONS    
# Set steps for p parameter in range 0 to 1
def p_steps_F():
    try:
        #p_step = float(input('\nEnter the step for the p parameter (i.e. 0.1): '))
        p_step = 0.1
    except:
        print('Invalid input!')
        p_step = 0.1

    p_list = []
    for p in np.arange(0+p_step, 1+p_step, p_step):
        p_list.append(round(p,3))
    
    return p_list, p_step

# Calculate Arrhenius
def calculate_arrhenius(data, data_names):
    x = -1
    data_arr = data

    p_list, p_step = p_steps_F()

    # Tables of calculated parameters
    r2_table_arr = pd.DataFrame(p_list, columns = ['p'])    # r2 is a correlation coeficient
    T0_table_arr = pd.DataFrame(p_list, columns = ['p'])    # T0 is a characteristic temp. deriviated from slope of function
    R0_table_arr = pd.DataFrame(p_list, columns = ['p'])    # R0 is a pre-exponential factor deriviated from intercept of function


    for i in data_names:
        x += 1
        data_arr = data

        temp_data = data_arr[x]
        new_data = temp_data.loc[:,['Temperatura [K]', 'Opor']]
        new_data['Ln(1/R)'] = np.log(1/new_data['Opor'])
        
        Y = new_data['Ln(1/R)']
        r2_list = []
        T0_list = []
        R0_list = []

        # Linear regression - looking for best fitting p parameter
        for p in np.arange(0+p_step, 1+p_step, p_step):
            column_p_name = 'p = ' + str(round(p,3))
            new_data[column_p_name] = 1/(new_data['Temperatura [K]']**p)
            X = new_data[column_p_name]
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
            del p_value
            del std_err
            r2_list.append(r_value**2)
            slope *= -1
            T0_list.append(slope**(1/p))
            R0_list.append(exp(-intercept))

        r2_table_arr[i] = r2_list
        T0_table_arr[i] = T0_list
        R0_table_arr[i] = R0_list
        data_arr[x] = new_data
    #print('\nCalculated r^2(p):\n', r2_table, '\n\nCalculated T0 parameter:\n', T0_table, '\n\nCalculated R0 parameter:\n', R0_table)

    print('\nMax values of r^2(p):')
    for i,j in enumerate(data_names):
        index_p = r2_table_arr[j].idxmax()
        max_r2 = r2_table_arr.iloc[index_p,i+1]
        param_p = r2_table_arr.iloc[index_p,0]
        param_T0 = T0_table_arr.iloc[index_p,i+1]
        param_R0 = R0_table_arr.iloc[index_p,i+1]
        print('%s. max r^2 = %.3f for p = %.2f, parameters T0 = %.2f, R0 = %.2f, for data %s' % (i+1,max_r2,param_p,param_T0,param_R0,j))

    return data_arr, r2_table_arr, p_list, p_step


# Calculate Differential Activation Energy (DAE)
def calculate_dae(data, data_names, p_list, p_step):
    data_dae = data
    Kb = constants.value('Boltzmann constant in eV/K') # 'Boltzmann constant' or '...in eV/K' or '...in Hz/K' or '...in inverse meter per kelvin'

    x = -1
    for i in data_names:
        x += 1

        temp_data = data_dae[x]
        new_data = temp_data.loc[:,['Temperatura [K]', 'Opor']]
        new_data['(Ln(R))'] = (np.log(temp_data['Opor']))
        new_data['d(Ln(R))'] = (new_data['(Ln(R))']).diff()
        new_data['(Kb*T)^(-1)'] = (temp_data['Temperatura [K]']*Kb)**(-1)
        new_data['d(Kb*T)^(-1)'] = (new_data['(Kb*T)^(-1)']).diff()
        new_data['DAE'] = new_data['d(Ln(R))']/new_data['d(Kb*T)^(-1)'] #DAE = d(Ln(R)) / d(Kb*T)^(-1)
           
        #print('\n',i,'\n',new_data)
        data_dae[x] = new_data 

    #for i,j in enumerate(data_names):
    #    print('\n',j,'\n',data_dae[i])

    return data_dae
