# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 16:25:09 2022

@author: cp17593
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:01:48 2022

@author: cp17593
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:17:41 2022

@author: cp17593
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 13:27:09 2022

alpha is the percentage of mismatches.
@author: cp17593
"""

import matplotlib.pyplot as plt
from scipy.special import binom
import matplotlib.font_manager as font_manager
import numpy as np

fontsize= 10
font = font_manager.FontProperties(family='CMU Serif', size=5)


def get_prob_same_keybits(blocksize, tau, alpha):
    ''''''
    assert tau <= np.ceil(blocksize/2) - 1
    probSum = 0
    for j in range(tau+1):
        binCoeff = binom(blocksize, j)
        result = binCoeff * ( alpha**j ) * ( ( 1-alpha )**(blocksize-j) )
        probSum += result
    
    return probSum


def get_prob_diff_keybits(blocksize, tau, alpha):
    ''''''
    assert tau <= np.ceil(blocksize/2) - 1

    start = int( blocksize - tau )
    finish = int(blocksize)
    probSum = 0
    for j in range(start, finish+1):
        binCoeff =int(binom(blocksize, j))
        result = binCoeff * ( alpha**j ) * ( ( 1-alpha )**(blocksize-j) )
        probSum += result

    return probSum


def get_prob_questionmark(blocksize, tau, alpha):
    ''''''
    assert tau <= np.ceil(blocksize/2) - 1
    start = int(tau + 1)
    finish = int(blocksize - tau -1)
    probSum = 0
    for j in range(start, finish +1):
        binCoeff = binom(blocksize, j)
        result = binCoeff * ( alpha**j ) * ( ( 1-alpha )**(blocksize-j) )

        probSum += result
    return probSum


def prob_matching_keys( blocksize, tau, m, alpha):
    '''gets the probability of matching key sequences. m is the size of the 
    original key at Alice.'''

    matching = get_prob_same_keybits(blocksize, tau, alpha)
    unknown = get_prob_questionmark(blocksize, tau, alpha)
    probMatch = (  matching + unknown )**m
    return  probMatch

def exp_length(blocksize, tau, alpha, lenghtOriginalKey):
    '''gets the expected length of the key'''
    questionmark= get_prob_questionmark(blocksize, tau, alpha)
    expLength= (lenghtOriginalKey)*(1-questionmark)
    return  expLength

def exp_missmatches(blocksize, tau, alpha, lenghtOriginalKey):
    '''gets the expected number of missmatches'''
    assert alpha < 0.5
    blocksize = int(blocksize)
    assert tau <= np.ceil(blocksize/2) - 1
    m = (lenghtOriginalKey)*get_prob_diff_keybits(blocksize, tau, alpha)
    
    return  m


def encoding_rate(blocksize, tau, alpha):
    assert tau <= np.ceil(blocksize/2) - 1
    p= get_prob_questionmark(blocksize, tau, alpha)
    
    return (1-p)/blocksize




def optimal_parameters_fixed_R(R, alpha):
    size = 60
    Rs = 8*np.ones((size,size))
    for n in range(2,size):
        for t in range(int(np.ceil(n/2))):
            Rs[n][t] = encoding_rate(n,t,alpha)- R
            if Rs[n][t] < 0:
                Rs[n][t] = 5
    place = np.argmin(Rs)
    blocksize = int(place/size)
    tau = place % size   
        
    return blocksize, tau


def key_disagreement_rate(blocksize, tau, alpha):
    assert tau <= np.ceil(blocksize/2) - 1
    a = exp_missmatches(blocksize, tau, alpha, 100)
    b = exp_length(blocksize, tau, alpha, 100)
    return a/b

def correlation(alpha):
    assert alpha < 0.5
    return (0.5-alpha)/0.5
                
   
def length_of_channel_seq(R, expFinalLength):
    '''input R: the key transmission rate '''
    return np.ceil(expFinalLength/R)


if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    
    #plot parameters
    plt.rcParams["font.family"] = 'CMU Sans Serif'  # comment out if problems
    plt.rcParams['font.size'] = 9
    figSize = (4,2)
    

    #thresholds = [1e-4]
    res = 30
    alphas = np.linspace(0.0,0.45,res)
    KDRates= np.ones(len(alphas))
    minBlocksizes = list(np.ones(len(alphas)))
    taus = list(np.ones(len(alphas)))
    lengthOfChannelSeq = list(np.ones(len(alphas)))
    expFinalLength = 128
   #
    #plt.figure(figsize = figSize)
    
    threshold = 0.01
 
    
    
    for i in range(len(alphas)):
            
        KDRates = np.ones(len(alphas))
        blocksizes = list(np.ones(len(alphas)))
        taus = list(np.ones(len(alphas)))
        rates = list(np.ones(len(alphas)))
        
            
        for i in range(len(alphas)):
            blocksizes[i], taus[i] = optimal_parameters_fixed_R(threshold, alphas[i])
            KDRates[i] = key_disagreement_rate(blocksizes[i],taus[i], alphas[i])
            rates[i] = encoding_rate(blocksizes[i],taus[i], alphas[i]) 
        
    gains = [d1 - d2 for d2, d1 in zip(KDRates, alphas)] 
            
    plt.plot(alphas, gains, '-', label = r'$R\geq{}$'.format(threshold))
  
    
    #plt.savefig("plot/graphs2_R_more_than{}.pdf".format(threshold), format="pdf", bbox_inches="tight")
    #plt.savefig("plot/graphs2_R_more_than{}.eps".format(threshold), format="eps", bbox_inches="tight")
            
        
        
    plt.xlabel(r'rates',fontsize= 9)
    plt.ylabel('gains', fontsize= 9)
    plt.xticks(alphas,fontsize=8)
    plt.yticks(fontsize=9)
    plt.title('Achieavable KDR'.format(threshold)) 
    plt.legend()

    plt.grid()


    