# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:23:42 2022

@author: cp17593
"""
import numpy as np
from random import randint

def isBinary(my_list):
    ''' Checks if a list (or tuple) is binary. Returns True or False.'''
    return set(my_list) == {0,1}


def keyAlice(length):
    "Generates a list of size 'length' with random binary inputs. This is the \
    secret (session) key generated at ALice."
    assert type(length) == int and length>0, "Argument must be a positive integer"
    return [randint(0,1) for i in range(length)]
    

def encrypt(key_alice,channel_seq_alice, block_size=3):
    ''' Inputs: key_alice: the binary session key created by Alice's PRNG 'keyAlice()'
                channel_seq_alice:  the binary channel sequence at Alice
                block_size:   determines the size of the blocks that the 
                channel_seq is grouped into for encryption
        Output: returns the ciphertext with size block_size*key'''
        
    assert isBinary(key_alice) == True , "Key must be binary"
    assert isBinary(channel_seq_alice) == True , "Sequence must be binary"
    assert len(key_alice)*block_size <= len(channel_seq_alice) , "The channel sequence is \
        not long enough. Inrease the length of the channel sequence, or reduce\
        the blocksize and/or the keysize."
    assert type(block_size) == int, "the second argument must be an integer"
    stretch_key =  np.repeat(key_alice, block_size) # stretches the length of the \
        # key to facilitate encyption by XoRing.     
        
    return [z[0]^z[1] for z in zip(stretch_key, channel_seq_alice)] 


def decrypt(channel_seq_bob, ciphertext,threshold ,block_size=3):
    ''' Inputs: channel_seq_bob:  the binary channel sequence at Bob
                ciphertext:  the encrypted sequence sent by Alice
                threshold:   the decision threshold(s) for hamming weights. It
                             comprises one or two integers (t1,t2).
                block_size:   determines the size of the blocks that the 
                channel_seq_bob is grouped into for encryption. This must match\
                the block-size used by Alice.
        Outputs: estimate_key: Bob's estimation of the key
                 bits2drop: there were some keybits that Bob was unsure about 
                 whether they were 0 or 1.  "bits2drop" is a list that indicates
                 the places of these list. Bob keeps this list for Alice: she needs
                 to know which bits to drop from the original key sequence'''     
    assert isBinary(ciphertext) == True , "2nd argument must be binary"
    assert isBinary(channel_seq_bob) == True , "1st argument must be binary"
    assert len(ciphertext) % block_size == 0, "Check that the first input is \
     the output of encrypt().Check that the block_size was the same in encrypt()."
    assert type(block_size) == int, "the second argument must be an integer"
    assert type(threshold) == int or len(threshold) == 2, "theshold must be an \
    integer or a list of two integers."
    
    global hamming_weights, xor_seq_grouped,xor_seq
    xor_seq = [s1^s2 for s1,s2 in zip(channel_seq_bob,ciphertext)]
    k = int(len(ciphertext) / block_size) # the length of the key
    xor_seq_grouped = np.array(xor_seq).reshape(k,block_size)
  
    hamming_weights = sum(xor_seq_grouped.T)
    #assert len(hamming_weights) == k
    estimate_key = np.ones(k) # initialise the key estimate
    bits2drop = [] # initiliase list that indicates the places for which Bob 
    #cannot make a decision about the keybit. The bits of these places will be 
    # dropped for the final key.
    if type(threshold)== int:
        t1, t2 = threshold, threshold + 1
    else:
        t1, t2 = threshold[0], threshold[1]
        assert type(t1) == int and type(t2) == int, "thresholds must be integers" 
        assert t2>=t1, "the second threshold cannot be smaller than the first"
    
    assert t2 <=block_size, "threshold cannot be larger than the block_size"
    for i in range(k):
        if hamming_weights[i] <= t1:
            estimate_key[i] = 0
        elif hamming_weights[i] >=t2:
            estimate_key[i] = 1
        else:
            bits2drop.append(i)    
            estimate_key[i] = 3 # "3" indicates uncertainty about the key. 
                                #This keybit will be dropped after the loop. 
    return list(estimate_key), bits2drop