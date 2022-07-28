#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copyright Chrysanthi Pascou, University of Bristol, 2022
Licence

Description 
   
Created on Wed Jul 27 14:48:35 2022

@author: cp17593
"""
#import sys
#sys.modules[__name__].__dict__.clear()

# Libraries ###################################################################
from SK_functions import encrypt, decrypt, keyAlice, genCorrSeq

# Constants ###################################################################
mismatches_dec = 0.1 # write in decimal
length_corr_sequence =1000
length_of_key = 100
block_size = 5
threshold = [1,4] # a good threshold is of the form: [n, blocksize - n]

# Main ########################################################################
if __name__ == '__main__':
    
    # give Alice and Bob two correlated sequences.    
    seq_alice, seq_bob = genCorrSeq(length_corr_sequence,mismatches_dec)
    
    # Alice generates a pseudorandom key of the enclosed length.
    key_alice= keyAlice(length_of_key) 
    
    #Alice encrypts the key.
    cipher = encrypt(key_alice,seq_alice, block_size)
        
    # Bob decrypts Alice's cipher
    key_bob, bits2drop = decrypt(seq_bob, cipher,threshold ,block_size)
    
    # Ideally "key_bob" consists of 0s and 1s. Any 3s  in key_bob indicates
    # that Bob does not know the binary values at those positions. All 3s must be
    # dropped. Bob needs to communicates the positions of 3s to Alice. 
    # This information is reserved in "bits2drop". The following two lines drop
    # those bits from both key-sequences at Alice and Bob.
    [key_alice.pop(b) for b in reversed(bits2drop)]
    [key_bob.pop(b) for b in reversed(bits2drop)]
 
    print("The two keys are symmetrical - {}".format(key_alice == key_bob))
        
    print(bits2drop)