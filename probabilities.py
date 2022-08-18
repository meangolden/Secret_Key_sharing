from urllib.parse import _ResultMixinBytes
import numpy as np
import scipy
from scipy.special import binom




class KeyStat():

    def __init__(self, alpha, n, m, tau):
        self.alpha=alpha
        self.n = n
        self.m = m
        self.tau = tau


    def get_prob_keyA_equal_keyB(self):

        probSum = 0
        for j in range(self.tau+1):
            binCoeff = binom(self.n, j)
            result = binCoeff * ( self.alpha**j ) * ( 1-self.alpha )**(self.n-j)

            probSum += result
        
        return probSum


    def get_prob_keyA_Notequal_keyB(self):

        start = self.n - self.tau
        finish = self.n
        probSum = 0

        for j in range(start, finish+1):
            binCoeff = binom(self.n, j)
            result = binCoeff * ( self.alpha**j ) * ( 1-self.alpha )**(self.n-j)

            probSum += result

        return probSum


    def get_prob_keyB_equal_unknown(self):
        start = self.tau + 1
        finish = self.n - self.tau -1
        probSum = 0
        for j in range(start, finish +1):
            binCoeff = binom(self.n, 128)
            result = binCoeff * ( self.alpha**j ) * ( 1-self.alpha )**(self.n-j)

            probSum += result
        return probSum

if __name__ == '__main__':
    alpha = 0.5
    n = 5000
    m = 128
    tau = 2
    stats = KeyStat(alpha, n, m, tau)
    print('key alice equal to key bob: ', stats.get_prob_keyA_equal_keyB())
    print('key alice not equal to key bob: ', stats.get_prob_keyA_Notequal_keyB())
    print('key bob equal to ?: ', stats.get_prob_keyB_equal_unknown())





