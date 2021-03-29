#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import matplotlib.pyplot as plt

# FUNCTIONS    
# Calculate
def do_plot(r2p, data_names):
    X = r2p.iloc[:, 0]
    if len(data_names) == 1:
        Y = r2p.iloc[:, 1]
        plt.scatter(X,Y)
        plt.title('r^2(p)')
        plt.show()
    elif len(data_names) == 2:
        fig, axs = plt.subplots(2)
        fig.suptitle('r^2(p)')
        axs[0].plot(X, r2p.iloc[:, 1])
        axs[0].set_title(data_names[0])
        axs[1].plot(X, r2p.iloc[:, 2])
        axs[1].set_title(data_names[1])
        fig.tight_layout()
    elif len(data_names) == 3:
        fig, axs = plt.subplots(2,2)
        fig.suptitle('r^2(p)')
        axs[0,0].plot(X, r2p.iloc[:, 1])
        axs[0,0].set_title(data_names[0])
        axs[0,1].plot(X, r2p.iloc[:, 2])
        axs[0,1].set_title(data_names[1])
        axs[1,0].plot(X, r2p.iloc[:, 3])
        axs[1,0].set_title(data_names[2])
        fig.tight_layout()
    elif len(data_names) == 4:
        fig, axs = plt.subplots(2,2)
        fig.suptitle('r^2(p)')
        axs[0,0].plot(X, r2p.iloc[:, 1])
        axs[0,0].set_title(data_names[0])
        axs[0,1].plot(X, r2p.iloc[:, 2])
        axs[0,1].set_title(data_names[1])
        axs[1,0].plot(X, r2p.iloc[:, 3])
        axs[1,0].set_title(data_names[2])
        axs[1,1].plot(X, r2p.iloc[:, 4])
        axs[1,1].set_title(data_names[3])
        fig.tight_layout()

    plt.show()
