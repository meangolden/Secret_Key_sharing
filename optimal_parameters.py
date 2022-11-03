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


def tx_key_rate(blocksize, tau, alpha):
    assert tau <= np.ceil(blocksize/2) - 1
    p= get_prob_questionmark(blocksize, tau, alpha)
    
    return (1-p)/blocksize

def key_disagreement_rate(blocksize, tau, alpha):
    assert tau <= np.ceil(blocksize/2) - 1
    a = exp_missmatches(blocksize, tau, alpha, 100)
    b = exp_length(blocksize, tau, alpha, 100)
    return a/b

def correlation(alpha):
    assert alpha < 0.5
    return (0.5-alpha)/0.5


def pass_sec_req(blocksize, tau, alpha, threshold= 1e-3 ):
    if key_disagreement_rate(blocksize, tau, alpha)< threshold:
        result = True
    else:
        result = False
    return result


def find_min_blocksize(tau, alpha, threshold= 1e-3):
       assert alpha < 0.5
       minBlocksize = max(2*tau+1,2) #initialise
       while key_disagreement_rate(minBlocksize, tau, alpha) > threshold:
           minBlocksize +=1
       assert tau <= np.ceil(minBlocksize/2)-1
       #assert minBlocksize < 76,   "blocksize is too large for computations"
       return minBlocksize 

def find_parameters(alpha, threshold= 1e-3):
       assert alpha < 0.5
       maxTestingTau = 10
       txKeyRates = list(np.ones(maxTestingTau))
       minBlocksize = list(np.ones(maxTestingTau))
       
       for tau in range(maxTestingTau):
           minBlocksize[tau] = find_min_blocksize(tau, alpha, threshold)
           txKeyRates[tau] = tx_key_rate(minBlocksize[tau],tau,alpha)
       tau_optimal = txKeyRates.index(max(txKeyRates))
       assert tau_optimal <= np.ceil(minBlocksize[tau_optimal]/2)-1
       
       return minBlocksize[tau_optimal], tau_optimal
   
def length_of_channel_seq(R, expFinalLength):
    '''input R: the key transmission rate '''
    return np.ceil(expFinalLength/R)


if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    
    #plot parameters
    plt.rcParams["font.family"] = 'CMU Sans Serif'  # comment out if problems
    plt.rcParams['font.size'] = 9
    figSize = (4,3)
    
    
    thresholds = [1e-2,1e-3, 1e-4 ,1e-5]
    #thresholds = [1e-4]
    res = 30
    alphas = np.linspace(0.0,0.499,res)

    
    plt.figure(figsize=figSize)
    
    for threshold in thresholds:
        
        #initialise
        keyTxRates = np.ones(len(alphas))
        minBlocksizes = list(np.ones(len(alphas)))
        taus = list(np.ones(len(alphas)))
        
       #
        
        for i in range(len(alphas)):
            
            (minBlocksizes[i], taus[i]) = find_parameters(alphas[i], threshold)
            keyTxRates[i] = tx_key_rate(minBlocksizes[i], taus[i], alphas[i])
    
      
        plt.plot(alphas, keyTxRates, label = r'KDR < {}'.format(threshold))
        plt.xlabel(r'$p$ch',fontsize= 9)
        plt.ylabel('$\mathbb{{E}}(R)$', fontsize= 9)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=9)
        #plt.title('Achievable rates') 
        plt.legend()
    
        plt.grid()
    #    plt.text(correlations[len(alphas)-]-0.1, keyTxRates[len(alphas)-]-0.005, str((minBlocksizes[i],taus[i])), fontsize=7)
        #for i in range(0,len(alphas)):                      
         #   plt.text(alphas[i]-0.04, keyTxRates[i]+0.015, str((minBlocksizes[i],taus[i])), fontsize=7)
            
        plt.savefig("plot/optimal_param.pdf", format="pdf", bbox_inches="tight")
        plt.savefig("plot/optimal_param.eps", format="eps", bbox_inches="tight")
            
        
        
    #2nd and 3rd plot

          
    threshold = 1e-3
    alphas = np.linspace(0.01,0.3,30) #channel mistmatch
    keyTxRates = np.ones(len(alphas))
    minBlocksizes = list(np.ones(len(alphas)))
    taus = list(np.ones(len(alphas)))
    lengthOfChannelSeq = list(np.ones(len(alphas)))
    expFinalLength = 128
   #
    
    for i in range(len(alphas)):
        
        (minBlocksizes[i], taus[i]) = find_parameters(alphas[i], threshold)
        keyTxRates[i] = tx_key_rate(minBlocksizes[i], taus[i], alphas[i])
        lengthOfChannelSeq[i] = length_of_channel_seq(keyTxRates[i], expFinalLength) 
        
    plt.figure(figsize = figSize)
    plt.plot(alphas, keyTxRates, '--o' )
    plt.xlabel(r'$p$ch',fontsize= 9)
    plt.ylabel('R', fontsize= 9)
    plt.xticks(alphas,fontsize=8)
    plt.yticks(fontsize=9)
    plt.title('Achieavable rates for KDR < {}'.format(threshold)) 
    plt.legend()

    plt.grid()

    for i in range(0,len(alphas)):                      
        plt.text(alphas[i]-0.025, keyTxRates[i]+0.005, str((minBlocksizes[i],taus[i])), fontsize=7)
    plt.savefig("plot/optimal_param_KDR_less_than{}.pdf".format(threshold), format="pdf", bbox_inches="tight")
    plt.savefig("plot/optimal_param_KDR_less_than{}.eps".format(threshold), format="eps", bbox_inches="tight")
    
    #3rd plot
    plt.figure(figsize = figSize)
    plt.plot(alphas[:-1], np.log10(lengthOfChannelSeq[:-1]), '--o' )
    for i in range(len(alphas[:-1])):                      
        plt.text(alphas[i]-0.015, np.log10(lengthOfChannelSeq[i])+0.1, str((minBlocksizes[i],taus[i])), fontsize=8)

    plt.xlabel(r'$p$ch',fontsize= 9)
    plt.ylabel('Length of channel sequence (mn)', fontsize= 9)
    plt.xticks(alphas,fontsize=8)
    plt.yticks(fontsize=9)
    plt.title('KDR < {}, $E(m)={}$'.format(threshold, expFinalLength),fontsize= 9) 
      
    
    #plt.savefig('Legnth_KDR_{}_$E(m)_{}$'.format(threshold, expFinalLength), format="pdf", bbox_inches="tight")
    #plt.savefig('Length_KDR_{}_$E(m)={}$'.format(threshold, expFinalLength), format="eps", bbox_inches="tight")
