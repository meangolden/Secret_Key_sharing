# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 18:46:02 2022

@author: cp17593
"""


import matplotlib.pyplot as plt
from scipy.special import binom
import matplotlib.font_manager as font_manager
import pandas as pd
import numpy as np


if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    alphas = [0.05,0.1,0.15,0.2,0.25,0.3]
    n_list = [7, 8, 9, 10, 11, 12]
    n_min = 5
    n_max = 10
    ms = [100]
    
    
    data = pd.DataFrame(columns=['m (length of)', 'alpha', 'n (block size)', 'tau (decision threshold)',
                'No_mism (expected number of mismatches)', 'L  (expected length of final key)', 
                'expected number of mismatches (%)'])
    length = []
    noMis = []
    lengthPerCent = []
    for alpha in alphas:
        for m in ms:
            stats = KeyStat(alpha, m)
            for n in n_list:
                for tau in range(1,int(n/2)+1):

                    length.append(stats.exp_length(n, tau))
                    noMis.append(stats.exp_missmatches(n,tau))
                    lengthPerCent.append(noMis/length*100)

    
                        # Append new data to excel
                    new_data = [m,alpha,n,tau,noMis,length, lengthPerCent]
                    wb = load_workbook('dataKeyGenStat.xlsx')
                    ws = wb.worksheets[0]
                    ws.append(new_data)
                    wb.save('ROC_complex.xlsx')
    
                    m_list = np.repeat(np.array([self.m]), len(tau_list)*len(n_list))
                    alpha_list = np.repeat(np.array([self.alpha]), len(tau_list)*len(n_list))
                    n_pd = np.tile(n_list, len(tau_list))
                    
                    
                    tau_list = np.array(tau_list)
                    tau_pd = np.repeat(tau_list, len(n_list))
            
            
                    data['m (length of)'] = m_list
                    data['alpha'] = alpha_list
                    data['n (block size)'] = n_pd
                    data['tau (decision threshold)'] = tau_pd
                    data['No_mism (expected number of mismatches)'] = noMis
                    data['L  (expected length of final key)'] = length
                    data['expected number of mismatches (%)'] = noMis/length*100
            
                    data.to_csv('dataKeyGenStat.csv')