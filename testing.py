#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 16:11:31 2022

Testing the relationship between Pearson correlation and percentage of bit 
agreement in binary sequences. 

@author: cp17593
"""

# Libraries ###################################################################
from SK_functions import genCorrSeq
import numpy as np
import matplotlib.pyplot as plt

# Constants ###################################################################
length = 1000

# Main ########################################################################
if __name__ == '__main__':
    mismatches_dec = np.linspace(0,1,500)
    pearson = np.ones(len(mismatches_dec))
    for i in range(len(mismatches_dec)):
        seq_alice, seq_bob = genCorrSeq(length, mismatches_dec[i])
        pearson[i]=(np.corrcoef(seq_alice,seq_bob)[0][1])
        
    capacity = [-log2(1-p**2) for p in np.linspace(0,0.999,20)]
    
    plt.plot(1-mismatches_dec, pearson)
