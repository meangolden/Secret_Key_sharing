#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copyright Chrysanthi Pascou, University of Bristol, 2022
Licence

Description: Alice wishes to share a secret key with Bob by communicating 
through a public channel. Alice and Bob share two correlated binary sequences.
Alice uses the correlated to Bob's sequence to 'hide' the secret key. For more
details: https://www.overleaf.com/read/dgsmpwkcxkfq

Created on Wed Jul 27 14:48:35 2022

@author: cp17593
"""
# Libraries ###################################################################
from SK_functions import encrypt, decrypt, keyAlice
from genKeys import getSequence

# Constants ###################################################################
# mismatches_dec = 0.2# write in decimal
length_corr_sequence =2000
length_of_key = 300
block_size = 7
threshold = 1 #the lower the threshold the higher the probability of two 
# matching keys (but also: more bits will be dropped)


filename = 'data3_upto5.mat' # dataset, copied from James's repo
window = 500 # window size
N = 7 # quantization, nuber of bits e.g. N=2: {00, 01, 10, 11}
var_factor = 2 # var_factor * (var of alice + var of bob) / 2
                # controlls the limit for quantization
verbose = True # if True shows some statistics of the seqeance

# Main ########################################################################
if __name__ == '__main__':
    
    #Give Alice and Bob two correlated sequences.    
    seq_alice, seq_bob = getSequence(filename, window, N, var_factor, verbose)
    no_missmatches = sum([i^j for i,j in zip(seq_alice, seq_bob)])
    agreem_sequences =1 - (no_missmatches/len(seq_alice))
    print('\n Channel sequences agree by \n', agreem_sequences)

    # seq_alice, seq_bob = genCorrSeq(length_corr_sequence,mismatches_dec)
    # print('\nseq_alice\n', type(seq_alice), len(seq_alice), seq_alice[:200])

    # Alice generates a pseudorandom key of the enclosed length.
    key_alice = keyAlice(length_of_key) 
    
    #Alice encrypts the key.
    cipher = encrypt(key_alice,seq_alice, block_size)
        
    #Bob decrypts Alice's cipher
    key_bob, bits2drop = decrypt(seq_bob, cipher,threshold ,block_size)
    
    # Ideally "key_bob" consists of 0s and 1s. Any 3s  in key_bob indicates
    # that Bob does not know the binary values at those positions. All 3s must be
    # dropped. Bob needs to communicates the positions of 3s to Alice. 
    # This information is reserved in "bits2drop". The following two lines drop
    # those bits from both key-sequences at Alice and Bob.
    [key_alice.pop(b) for b in reversed(bits2drop)]
    [key_bob.pop(b) for b in reversed(bits2drop)]

    print('\n\n\n Channel Sequences\n')
    print("Alice's and Bob's channel sequences agree by ",agreem_sequences)
    
    
   # print('key_alice ', key_alice)
   # print('key_bob ', key_bob)
    print("Drop bits in places:{}".format(bits2drop))
    print("The two keys are symmetrical - {}".format(key_alice == key_bob))
        
    if key_alice != key_bob:
        number_mismatches = sum([i^j for i,j in zip(key_alice,key_bob)])
        print("Key Disagreement percentage is {}".format(number_mismatches / len(key_alice)))
    print("The length of the new key is {}".format(len(key_alice))) 
