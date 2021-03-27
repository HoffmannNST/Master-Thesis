#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import pathlib

# Predefined settings
loaded_files=[]
data =[]

# FUNCTIONS
# Import file
def import_file():
    while True:
        #data_path = input('\nSpecify folder path (data_test_folder/Pomiar1):\n')
        data_path = 'data_test_folder/Pomiar 1'

        if pathlib.Path(data_path).exists() == True:
            #delimeter = input('\nSpecify columns separator (i.e. symbol [, ; .] or \t for tab):\n')     # /t - tab
            delimeter = '\t'
            #coma = input('\nSpecify decimal separator in the files:\n')     # '.' or ','
            coma = ','

            data_path1 = data_path+'/Grzanie/grzaniePomiar_Keithley2400.txt'
            data_path2 = data_path+'/Grzanie/grzaniePomiar_Keithley2000.txt'
            data_path3 = data_path+'/Chłodzenie/chlodzeniePomiar_Keithley2400.txt'
            data_path4 = data_path+'/Chłodzenie/chlodzeniePomiar_Keithley2000.txt'

            file_names = [data_path1, data_path2, data_path3, data_path4]
            
            for i in file_names:
                if pathlib.Path(i).exists() == True:
                    data.append(pd.read_csv(i, sep =delimeter, decimal =coma, header =0))
                    loaded_files.append(i)

            print('\nFiles loaded:')
            for count, item in enumerate(loaded_files, 0):
                print(count, item)
            return data, loaded_files, delimeter, coma
                    
        else:
            input('\nSpecified path does not exist!\nPress ENTER to continue...')
