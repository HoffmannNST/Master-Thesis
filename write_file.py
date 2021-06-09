#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib

# FUNCTIONS
# Export file
def save_file(data_arr, data_dae, data_names, delimeter :str, coma :str, r2_table):
    x = -1
    saved_files = []

    pathlib.Path('Results/Arrhenius').mkdir(parents=True, exist_ok=True)
    pathlib.Path('Results/DAE').mkdir(parents=True, exist_ok=True)

    # Save Arrhenius data
    r2_table.to_csv('Results/Arrhenius/r2p_arr.txt', index=False, sep =delimeter, decimal =coma)
    saved_files.append('Results/Arrhenius/r2p_arr.txt')
    for i in data_names:
        x += 1
        data_temp = data_arr[x]
        data_path = 'Results/Arrhenius/' + i + '.txt'     
        data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
    
        saved_files.append(data_path)

    # Save DAE data
    x = -1
    for i in data_names:
        x += 1
        data_temp = data_dae[x]
        data_path = 'Results/DAE/' + i + '.txt'     
        data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
    
        saved_files.append(data_path)

    print('\nFiles saved:')
    for count, item in enumerate(saved_files, 0):
        print(count, item)
    return
