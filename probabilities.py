from urllib.parse import _ResultMixinBytes
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.special import binom




class KeyStat():

    def __init__(self, alpha, m):
        '''n and tau have to be local'''
        self.alpha=alpha

        self.m = m



    def get_prob_keyA_equal_keyB(self, n,  tau):
        ''''''
        probSum = 0
        for j in range(tau+1):
            binCoeff = binom(n, j)
            result = binCoeff * ( self.alpha**j ) * ( ( 1-self.alpha )**(n-j) )

            probSum += result
        
        return probSum


    def get_prob_keyA_Notequal_keyB(self, n, tau):
        ''''''

        start = n - tau
        finish = n
        probSum = 0

        for j in range(start, finish+1):
            
            binCoeff = binom(n, j)
            result = binCoeff * ( self.alpha**j ) * ( ( 1-self.alpha )**(n-j) )

            probSum += result

        return probSum


    def get_prob_keyB_equal_unknown(self, n, tau):
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
        '''gets the probability of matching and mismatching keys'''

        matching = self.get_prob_keyA_equal_keyB(n, tau)
        unknown = self.get_prob_keyB_equal_unknown(n, tau)
        probMatch = (  matching + unknown )**self.m
        return  probMatch
    
    def length_of_keys(self, n, tau):
        '''gets the expected length of the key'''
        prob_missmatching = 1 - self.get_prob_matching_keys(n, tau)
        expLength= (self.m)- self.m*prob_missmatching
        return  expLength
    
    def plot(self, n_list, tau_list):
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