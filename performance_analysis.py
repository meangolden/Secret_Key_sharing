# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 21:16:46 2022

@author: cp17593
"""

import matplotlib.pyplot as plt
from scipy.special import binom


class KeyStat():

    def __init__(self, alpha, m=300):
        '''n and tau have to be local'''
        self.alpha=alpha
        self.m = m


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
                     
            plt.plot(n_list, probMatch, label=f'tau= {tau}')
            #plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xlabel('Block size length')
        plt.ylabel('Probability of two matching keys')
        plt.title(f'alpha= {self.alpha}, m= {self.m}')
        plt.grid()
        plt.legend()
        
        
        
    def plot_exp_no_missmathces(self, n_list, tau_list):
        '''Very simple plotting method'''
        plt.figure()
        for tau in tau_list:
            ys= []
            #probMismatch = []
            for n in n_list:
                y= self.exp_missmatches(n, tau)
                ys.append(y)
                 
            plt.plot(n_list, ys, label=f'tau= {tau}')
        #plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xlabel('Block size length')
        plt.ylabel('Expected Number of Missmatches')
        plt.title(f'alpha= {self.alpha}, m= {self.m}')
        plt.grid()
        plt.legend()
        
    def plot_exp_length(self, n_list, tau_list):
        '''Very simple plotting method'''
        plt.figure()
        for tau in tau_list:
            ys= []
            #probMismatch = []
            for n in n_list:
               y= self.exp_length(n, tau)
               ys.append(y)
               
    def plot_everything(self, n_list, tau_list):
        self.plot_exp_no_missmathces(n_list, tau_list)
        self.plot_exp_length(n_list, tau_list)
        self.plot_exp_no_missmathces(n_list, tau_list)  

        