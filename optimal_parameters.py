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

fontsize= 9
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
    start =blocksize - tau
    finish = blocksize
    probSum = 0
    for j in range(start, finish+1):
        binCoeff = binom(blocksize, j)
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

def exp_missmatches(blocksize, tau, lenghtOriginalKey, alpha):
    '''gets the expected number of missmatches'''
    assert tau <= np.ceil(blocksize/2) - 1
    missmatches= (lenghtOriginalKey)*get_prob_diff_keybits(blocksize, tau, alpha)
    return  missmatches


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
       assert key_disagreement_rate(minBlocksize, tau, alpha) < threshold
       assert tau <= np.ceil(minBlocksize/2)-1
       
       return minBlocksize 

def find_parameters(alpha, threshold= 1e-3):
       assert alpha < 0.5
       maxTestingTau = 30
       txKeyRates = list(np.ones(maxTestingTau))
       minBlocksize = list(np.ones(maxTestingTau))
       
       for tau in range(maxTestingTau):
           minBlocksize[tau] = find_min_blocksize(tau, alpha, threshold)
           txKeyRates[tau] = tx_key_rate(minBlocksize[tau],tau,alpha)
       tau_optimal = txKeyRates.index(max(txKeyRates))
       
       assert tau_optimal <= np.ceil(minBlocksize[tau_optimal]/2)-1
       return minBlocksize[tau_optimal], tau_optimal


if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    
    #plot parameters
    plt.rcParams["font.family"] = 'CMU Sans Serif'  # comment out if problems
    plt.rcParams['font.size'] = 9
    figSize = (4,2)
    
    
    # plot KDR vs correlation. KDR as a function of the alpha(correlation). Fix tau and blocksize

    #plt.figure(figsize = figSize)
#    res = 10
#    alphas = np.linspace(0.1,0.49,res)
#    correlations = [correlation(alpha) for alpha in alphas]
#    keyDisRates = np.ones(res) #initialise
#    keyTxRates = np.ones(res) 

#    for tau in range(int(np.ceil(blocksize/2))):
#        for i in range(len(correlations)):
#            keyDisRates[i] = key_disagreement_rate(blocksize, tau, alphas[i])
#                        
#        plt.plot(correlations, keyDisRates, '-', label = r'$\tau$ = {}'.format(tau))
#        #plt.plot(n_list, probMismatch, label='key mismatch prob')
#  #  plt.xticks(n_list)
#    plt.xlabel('Correlation')
#    plt.ylabel('Key Disagreement Rate')
#    plt.title(r'blocksize = {}'.format(blocksize),fontsize=11)
#  #  plt.grid()
#    plt.legend(fontsize=10)
#  #  plt.savefig(f"plot/matchingKeys_alp{alpha}_m{m}.pdf", format="pdf", bbox_inches="tight")
#  #  plt.savefig(f"plot/matchingKeys_alp{alpha}_m{m}.eps", format="eps")
#    
#    plt.figure(figsize = figSize)
#    for tau in range(int(np.ceil(blocksize/2))):
#        for i in range(len(correlations)):
#            keyTxRates[i] = tx_key_rate(blocksize, tau, alphas[i])
#                    
#        plt.plot(correlations, keyTxRates, '-', label = r'$\tau$ = {}'.format(tau))
#    #plt.plot(n_list, probMismatch, label='key mismatch prob')
#  #  plt.xticks(n_list)
#    plt.xlabel('Correlation')
#    plt.ylabel('Key Transmission Rate')
#    plt.title(r'blocksize = {}'.format(blocksize),fontsize=11)
# #  plt.grid()
#    plt.legend(fontsize=10)
# #  plt.savefig(f"plot/matchingKeys_alp{alpha}_m{m}.pdf", format="pdf", bbox_inches="tight")
# #  plt.savefig(f"plot/matchingKeys_alp{alpha}_m{m}.eps", format="eps")
#     
 # Second plot
#    minBlocksize = np.ones(len(alphas)) 
#    keyTxRates = np.ones(len(alphas)) 
#    threshold= 1e-3
#
#    
#    plt.figure(figsize = figSize)
#    for tau in [0,2,4,6]:
#        for i in range(len(alphas)):
#             minBlocksize[i] = find_min_blocksize(tau, alphas[i], threshold)
#             keyTxRates[i] = tx_key_rate(minBlocksize[i], tau, alphas[i])
#        print(minBlocksize)
#
#        plt.plot(alphas, keyTxRates, '-', label = r'$\tau$ = {}'.format(tau))
#        plt.xlabel(r'$\alpha$')
#        plt.ylabel('Acheivable Key Transmission Rate')
#        plt.title(r'KDR < {}'.format(threshold),fontsize=11)
#     #  plt.grid()
#        plt.legend(fontsize=10)
 
 #  Third plot
    
    threshold= 1e-5
    #res = 30
    #alphas = np.linspace(0.05,0.49,res)
    alphas = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
    keyTxRates = np.ones(len(alphas)) 

    correlations = [correlation(alpha) for alpha in alphas]
    minBlocksizes = list(np.ones(len(alphas)))
    taus = list(np.ones(len(alphas)))
    plt.figure(figsize = figSize)
    for i in range(len(alphas)):
        (minBlocksizes[i], taus[i]) = find_parameters(alphas[i], threshold)
        keyTxRates[i] = tx_key_rate(minBlocksizes[i], taus[i], alphas[i])

    alphas = correlations
    plt.plot(correlations, keyTxRates, '--o')
    plt.xlabel(r'$\rho$',fontsize=9)
    plt.ylabel('Key Tx Rate',fontsize=9)
    plt.xticks(alphas, fontsize=8)
    plt.yticks([0.0,0.05,0.1,0.15,0.2,0.25],fontsize=9)
    plt.title(r'KDR < {}'.format(threshold),fontsize=9)
    plt.grid()
    
    
#    plt.text(correlations[len(alphas)-]-0.1, keyTxRates[len(alphas)-]-0.005, str((minBlocksizes[i],taus[i])), fontsize=7)
    for i in range(0,len(alphas)):
        #s1 = r'$n={}$'.format(minBlocksizes[i])
        #plt.text(alphas[i] + 0.005, keyTxRates[i]+0.025, s1)
        #s2 = r'$\tau = {}$'.format(taus[i])
        #plt.text(alphas[i] + 0.005, keyTxRates[i], s2)
        plt.text(correlations[i]-0.04, keyTxRates[i]+0.015, str((minBlocksizes[i],taus[i])), fontsize=7)
        
        plt.savefig("plot/optimal_param_KDR_less_than{}.pdf".format(threshold), format="pdf", bbox_inches="tight")
        plt.savefig("plot/optimal_param_KDR_less_than{}.eps".format(threshold), format="eps", bbox_inches="tight")
        
    print(minBlocksizes)
    print("--------------")
    print(taus)