# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 21:16:46 2022
@author: cp17593
"""

import matplotlib.pyplot as plt
from scipy.special import binom
import matplotlib.font_manager as font_manager
import pandas as pd
import numpy as np


class KeyStat():

    def __init__(self, alpha, m=100):
        '''n and tau have to be local'''
        self.alpha=alpha
        self.m = m
        self.fontsize=11
        self.NoMis = []
        self.length = []
        self.font = font_manager.FontProperties(family='CMU Serif', size=11)


    def get_prob_same_keybits(self, n,  tau):
        ''''''
        probSum = 0
        for j in range(tau+1):
            binCoeff = binom(n, j)
            result = binCoeff * ( self.alpha**j ) * ( ( 1-self.alpha )**(n-j) )
            probSum += result
        
        return probSum


    def get_prob_diff_keybits(self, n, tau):
        ''''''
        start = n - tau
        finish = n
        probSum = 0
        for j in range(start, finish+1):
            binCoeff = binom(n, j)
            result = binCoeff * ( self.alpha**j ) * ( ( 1-self.alpha )**(n-j) )
            probSum += result

        return probSum


    def get_prob_questionmark(self, n, tau):
        ''''''
        start = tau + 1
        finish = n - tau -1
        probSum = 0
        for j in range(start, finish +1):
            binCoeff = binom(n, j)
            result = binCoeff * ( self.alpha**j ) * ( ( 1-self.alpha )**(n-j) )

            probSum += result
        return probSum


    def prob_matching_keys(self, n, tau):
        '''gets the probability of matching key sequences'''

        matching = self.get_prob_same_keybits(n, tau)
        unknown = self.get_prob_questionmark(n, tau)
        probMatch = (  matching + unknown )**self.m
        return  probMatch
    
    def exp_length(self, n, tau):
        '''gets the expected length of the key'''
        questionmark= self.get_prob_questionmark(n, tau)
        expLength= (self.m)- self.m*questionmark
        return  expLength
    
    def exp_missmatches(self, n, tau):
        '''gets the expected number of missmatches'''
        missmatches= (self.m)*self.get_prob_diff_keybits(n, tau)
        return  missmatches

    # plotting
    def plot_prob_matching_keys(self, n_list, tau_list):
        '''Very simple plotting method'''
        plt.figure()
        for tau in tau_list:
            probMatch = []
            #probMismatch = []
            for n in n_list:
                pdfMatch= self.prob_matching_keys(n, tau)
                probMatch.append(pdfMatch)
                     
            plt.plot(n_list, probMatch, '--o', label = r'$\tau$ = {}'.format(tau))
            #plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xticks(n_list)
        plt.xlabel('Block size length')
        plt.ylabel('Probability of two matching keys')
        #plt.title(r'$\alpha$= {}, m= {}'.format(self.alpha,self.m),fontsize=11)
        plt.grid()
        plt.legend(fontsize=10)
        plt.savefig(f"plot/matchingKeys_alp{self.alpha}_m{self.m}.pdf", format="pdf", bbox_inches="tight")
        plt.savefig(f"plot/matchingKeys_alp{self.alpha}_m{self.m}.eps", format="eps")
        
        
        
    def plot_exp_no_missmathces(self, n_list, tau_list):
        '''Very simple plotting method'''
        plt.figure()
        for tau in tau_list:
            ys= []
            #probMismatch = []
            for n in n_list:
                y= self.exp_missmatches(n, tau)
                ys.append(y)
                self.NoMis.append(round(y, 4))
                 
            plt.plot(n_list, ys, '--o', label= r'$\tau$ = {}'.format(tau))
        #plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xticks(n_list)
        plt.xlabel('Block size length')
        plt.ylabel('Expected Number of Missmatches')
        #plt.title(r'$\alpha$= {}, $m$= {}'.format(self.alpha,self.m),fontsize=11)
        plt.grid()
        plt.legend()
        plt.savefig(f"plot/expNoMissmathces_alp{self.alpha}_m{self.m}.pdf", format="pdf", bbox_inches="tight")
        plt.savefig(f"plot/expNoMissmathces_alp{self.alpha}_m{self.m}.eps", format="eps")
        
    def plot_exp_length(self, n_list, tau_list):
        '''Very simple plotting method'''
        plt.figure()
        for tau in tau_list:
            ys= []
            #probMismatch = []
            for n in n_list:
               y= self.exp_length(n, tau)
               ys.append(y)
               self.length.append(round(y, 4))
             
            plt.plot(n_list, ys, '--o', label= r'$\tau$ = {}'.format(tau))
        #plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xticks(n_list)
        plt.xlabel('Block size length')
        plt.ylabel('Expected length of key sequence')
        #plt.title(r'$\alpha=$ {}, $m$= {}'.format(self.alpha,self.m),fontsize=11)
        plt.grid()
        plt.legend()
        plt.savefig(f"plot/expLength_alp{self.alpha}_m{self.m}.pdf", format="pdf", bbox_inches="tight")
        plt.savefig(f"plot/expLength_alp{self.alpha}_m{self.m}.eps", format="eps")


    def plot_everything(self, n_list, tau_list):
        self.plot_exp_length(n_list, tau_list)
        self.plot_exp_no_missmathces(n_list, tau_list)
        self.plot_prob_matching_keys(n_list, tau_list)



    def createDataframe(self, n_list, tau_list):
        tau_list = np.array(tau_list)
        n_list = np.array(n_list)
        length = np.array(self.length)
        noMis = np.array(self.NoMis)
        data = pd.DataFrame(columns=['m (length of)', 'alpha', 'n (block size)', 'tau (decision threshold)',
        'No_mism (expected number of mismatches)', 'L  (expected length of final key)', 
        'expected number of mismatches (%)'])
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

if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    
    plt.rcParams["font.family"] = 'CMU Sans Serif'  # comment out if problems
    plt.rcParams['font.size'] = 12
    
    alpha = 0.1
    n_list = [7, 8, 9, 10, 11, 12]
    m = 100
    tau_list = [1, 2, 3]
    stats = KeyStat(alpha, m)
    stats.plot_everything(n_list, tau_list)
    stats.createDataframe(n_list, tau_list) # this function reuses parts of plot_everything
    plt.show()
