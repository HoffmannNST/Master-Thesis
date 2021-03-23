#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import numpy as np

# Predefined settings
data = []

# FUNCTIONS    
# Calculate
def calculate(data, loaded_files):
    x = -1
    for i in loaded_files:
        x += 1
        data_temp = data[x]
        new_data = data_temp.loc[:,['Temperatura [K]', 'Opor']]

        new_data['Ln(1/R)'] = np.log(1/new_data['Opor'])

        try:
            p_step = float(input('Enter the step for the p parameter (i.e. 0.1): '))
            #p_step = 0.1
        except:
            print('Invalid input!')
            p_step = 0.1
        
        for p in np.arange(0+p_step, 1+p_step, p_step):
            new_data[str(round(p,3))] = 1/(new_data['Temperatura [K]']**p)
        print('\nData from file:\n%s\n\n%s' %(i,new_data))
        data[x] = new_data

    return data
