# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:48:35 2022

@author: cp17593
"""
###############################################################################
# Libraries
###############################################################################
from SK_functions import encrypt, decrypt, isBinary, keyAlice

###############################################################################
# Input parameters
###############################################################################
channel_seq_alice = aliceKey
channel_seq_bob = bobKey
block_size = 4
threshold = [1,3]

###############################################################################
# Main
###############################################################################
if __name__ == '__main__':
    #Alice generates a pseudorandom key of the enclosed length.
    key_alice= keyAlice(100) 
    print(key_alice)
    
    #Alice encrypts the key.
    cipher = encrypt(key_alice,channel_seq_alice, block_size)
    
    
    #Bob decrypts Alice's cipher
    key_bob, bits2drop = decrypt(channel_seq_bob, cipher,threshold ,block_size)
    
    print(key_bob)
    #Ideally "key_bob" consists of 0s and 1s. Any 3s  in key_bob indicates
    #that Bob does not know the binary values at those positions. All 3s must be
    #dropped. Bob needs to communicates the positions of 3s to Alice. 
    #This information is reserved in "bits2drop". The following two lines drop
    #those bits from both key-sequences at Alice and Bob.
    [key_alice.pop(b) for b in reversed(bits2drop)]
    [key_bob.pop(b) for b in reversed(bits2drop)]
    
    print(key_alice)
    print(key_bob)
    key_alice == key_bob
        
    