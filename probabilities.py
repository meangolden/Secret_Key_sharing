from urllib.parse import _ResultMixinBytes
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.special import binom




class KeyStat():

    def __init__(self, alpha, m):
        '''n and tau have to be local'''
        self.alpha=alpha
        self.n = n
        self.m = m
        self.tau = tau


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
        ''''''

        matching = self.get_prob_keyA_equal_keyB(n, tau)
        unknown = self.get_prob_keyB_equal_unknown(n, tau)

        probMatch = (  matching + unknown )**self.m
        probMismatch = 1 - probMatch

        

        return  probMatch, probMismatch

    
    def plot(self, n_list, tau):
        ''''''
        match = []
        mismatch = []
        for n in n_list:
            pdfMatch, pdfMismatch = self.prob_matching_keys(n, tau)
            match.append(pdfMatch)
            mismatch.append(mismatch)

        plt.plot(match, n_list, label='key match prob')
        plt.plot(mismatch, n_list, label='key mismatch prob')
        plt.xlabel('Block size length')
        plt.ylabel('Probability')
        plt.legend()
        plt.show()

    

if __name__ == '__main__':
    alpha = 0.1
    n = [5000, 6000, 1000]
    m = 10
    tau = 2
    stats = KeyStat(alpha, m)






