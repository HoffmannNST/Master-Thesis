#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Predefined settings
data = []

# FUNCTIONS    
# Calculate
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

    r2p = pd.DataFrame(p_list, columns = ['p'])     # r2p stands for function r^2(p)

    for i in data_names:
        x += 1

        temp_data = data[x]
        new_data = temp_data.loc[:,['Temperatura [K]', 'Opor']]
        new_data['Ln(1/R)'] = np.log(1/new_data['Opor'])
        
        regr = LinearRegression()
        Y = new_data['Ln(1/R)'].values.reshape(-1,1)
        r2_scores = []

        for p in np.arange(0+p_step, 1+p_step, p_step):
            column_p_name = '1/T^(' + str(round(p,3)) + ')'
            new_data[column_p_name] = 1/(new_data['Temperatura [K]']**p)
            X = new_data[column_p_name].values.reshape(-1,1)
            regr.fit(X, Y)
            score = regr.score(X, Y)
            r2_scores.append(score)
        
        r2p[i] = r2_scores
        data[x] = new_data

    print('\nCalculated r^2(p):\n', r2p)

    print('\nMax values of r^2(p):\n')
    for i,j in enumerate(data_names):
        find_max_p = r2p[j]
        index_p = find_max_p.idxmax()
        max_r2 = find_max_p[index_p]
        max_p = r2p.iloc[0,index_p]
        print('%s. max r^2 = %.3f for p = %.2f for data %s' % (i+1,max_r2,max_p,j))

    return data, r2p

def calculate_dae():
    pass
