# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:14:06 2022
This code has shown that (KDR) can be approximated with Px / (1-P?) :) 
F a n t a s t i c !!!!!!!!!!! 
It shows the variance from the expected value :)
@author: cp17593
"""
import matplotlib.pyplot as plt
import numpy as np
from SK_functions import genCorrSeq, encrypt, decrypt, keyAlice, KDR_KTR

block_size = 10
tau = 2
lenght_of_key = 50
iterations = 1000
length = 3000 # the lenght of channel sequence
mismatches_dec = 0.4

# Give Alice the initial key
key_alice = keyAlice(lenght_of_key)
KDRs = np.ones(iterations)
KTRs = np.ones(iterations)

for i in range(iterations):
    # Give Alice and Bob two correlated channel sequences
    sa, sb =  genCorrSeq(length, mismatches_dec)
    
    # encrypt and decrypt
    ciphertext = encrypt(key_alice, sa, block_size)
    bob_estimate, places2drop = decrypt(sb, ciphertext, tau, block_size)
    
    #find the Key Disagreement Rate:
    KDRs[i], KTRs[i]=  KDR_KTR(key_alice, bob_estimate, block_size)


#print(np.mean(KDRs))
print(np.var(KDRs))
#print(np.mean(KTRs))
print(np.var(KTRs))