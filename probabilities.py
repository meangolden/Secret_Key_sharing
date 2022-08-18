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
        probMismatch = 1 - probMatch

        

        return  probMatch, probMismatch

    
    def plot(self, n_list, tau):
        '''Very simple plotting method'''
        probMatch = []
        probMismatch = []
        for n in n_list:
            pdfMatch, pdfMismatch = self.prob_matching_keys(n, tau)
            probMatch.append(pdfMatch)
            probMismatch.append(pdfMismatch)

        fig = plt.figure()
        plt.plot(n_list, probMatch, label='key match prob')
        plt.plot(n_list, probMismatch, label='key mismatch prob')
        plt.xlabel('Block size length')
        plt.ylabel('Probability')
        plt.title(f'tau: {tau}')
        plt.grid()
        plt.legend()



    def getGraphs(self, n_list, tau_list):
        '''makes plots for various tau's'''
        for tau in tau_list:
            self.plot(n_list, tau)

        

    

if __name__ == '__main__':
    '''runs the whole thing, alpha and tau need to be in an array'''
    alpha = 0.1
    n_list = [5, 6, 7, 8, 9, 10]
    m = 300
    tau_list = [1, 2, 3]
    stats = KeyStat(alpha, m)
    stats.getGraphs(n_list, tau_list)
    plt.show()





