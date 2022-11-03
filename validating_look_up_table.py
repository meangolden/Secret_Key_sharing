# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 13:47:09 2022

@author: cp17593

Validating the choice of parameteres. Parameterisation lives
in the Look up table "Optimal_parameters"
To run this code, you need access to two files:
    1. SK_functions.py
    2. Optimal_parameters.xlsx
"""
# python libraries
import numpy as np
import pandas as pd

# local libraries
import SK_functions as sk


if __name__ == '__main__':
    
    length_of_initial_key = 128
    sample_size_ch_mismatch = 16
    rep = 100 # times for repeating the key agreement
    
    
    KDR = [] # vector to store KDR
    for _ in range(rep):
        # Give Alice and Bob two correlated sequences.#############################
        # In reality, these sequences are derived through measurements of the
        # reciprocal RF channel between Alice and Bob, e.g. RSS measusements.   
        ch_mismatch = (1 - np.random.rand(1))*.3 # a random number between 0 & 0.3.    
        ch_seq_A, ch_seq_B = sk.genCorrSeq(int(1e4), ch_mismatch)
        
        # Estimate ch_mismatch
        sampleA = ch_seq_A[0:64]
        sampleB = ch_seq_B[0:64]
        est_pch = sum([i != j for i,j in zip(sampleA, sampleB)])/len(sampleA)
        
        # exclude the sample from the channel sequences
        ch_seq_A, ch_seq_B  = ch_seq_A[64:], ch_seq_B[64:]
        
        # Based on the estimation of channel mismatch (est_ch), choose parameters
        # from the look up table
        look_up = pd.read_excel("Optimal_parameters.xlsx")
        pch = look_up.values[:,0]
        
        indx = 0
        if est_pch>= 0.3:
            indx = -1 # to indicate the last row of the look up table
        else:
            while est_pch > pch[indx]:
                indx +=1
        block_size = look_up.values[indx, 1]
        tau = look_up.values[indx, 2]      
        
        
        # Alice generates a pseudorandom key of the enclosed length. Then Alice
        # encrypts the key. 
        key_alice = sk.keyAlice(length_of_initial_key) 
        cipher = sk.encrypt(key_alice,ch_seq_A, block_size)
        # Bob decrypts Alice's cipher
        key_bob, bits2drop = sk.decrypt(ch_seq_B, cipher,tau ,block_size)
        
        # Drop the uncertain bits. I.e. the bits with index in "bits2drop".
        [key_alice.pop(b) for b in reversed(bits2drop)]
        [key_bob.pop(b) for b in reversed(bits2drop)]
        
        # Find the key disagreement rate
        no_correct_bits = sum([a == b for a,b in zip(key_alice, key_bob)])
        KDR.append((len(key_alice) - no_correct_bits)/len(key_alice))
        

    print("KDRs: ", KDR)
    print("average KDR: ", sum(KDR)/len(KDR))
        
    
    
    
    