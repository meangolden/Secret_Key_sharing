# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:23:42 2022
['A' for _ in range(5)]
@author: cp17593
"""
import numpy as np
from random import randint, sample

def isBinary(my_list):
    ''' Checks if a list (or tuple) is binary (0s and 1s). Returns True or False.
    '''
    return (set(my_list) == {0,1}) or (set(my_list) == {0}) or (set(my_list) == {1}) 


def keyAlice(length):
    '''Generates a list of size 'length' with random binary inputs. This is the
    secret (session) key generated at ALice.
    '''
    assert type(length) == int and (length > 0), \
        "Argument must be a positive integer"
        
    return [randint(0, 1) for _ in range(length)]
    

def encrypt(key_alice,channel_seq_alice, block_size=3):
    ''' Alices encrypts her secret key by utilising her channel sequence.
    The channel sequence is grouped in groups of 'block_size'. Alice generates
    a new sequence by flipping or not each group. Every time the key bit is 1, 
    the corresponing group of bits will be flipped. If the key bit is 0, the 
    corresponding group will not be passed on the new sequence unaltered.
    
    Inputs: key_alice: the binary session key created by Alice's PRNG 'keyAlice()'
        channel_seq_alice:  the binary channel sequence at Alice
            block_size:   determines the size of the blocks that the 
                channel_seq is grouped into for encryption
    Output: returns the ciphertext with size block_size*key
    '''
    assert isBinary(key_alice) == True , "Key must be binary"
    assert isBinary(channel_seq_alice) == True , "Sequence must be binary"
    assert len(key_alice)*block_size <= len(channel_seq_alice) , "Channel sequence is \
        not long enough. Inrease the length of the channel sequence, or reduce\
        the blocksize and/or the keysize."
    assert type(block_size) == int, "Second argument must be an integer"
    
    # stretches the length of the key to facilitate encyption by XoRing. 
    stretch_key =  np.repeat(key_alice, block_size)  
        
    return [z[0]^z[1] for z in zip(stretch_key, channel_seq_alice)] 


def decrypt(channel_seq_bob, ciphertext, threshold, block_size=3):
    '''Bob decrypts the cipher sent by Alice in order to retrieve the secret key. 
    
        Inputs: channel_seq_bob:  the binary channel sequence at Bob
                ciphertext:  the encrypted sequence sent by Alice
                threshold:   the decision threshold(s) for hamming weights. It
                             comprises one or two integers (t1,t2).
                block_size:   determines the size of the blocks that the 
                channel_seq_bob is grouped into for encryption. This must match
                the block-size used by Alice.
        Outputs: estimate_key: Bob's estimation of the key
                 bits2drop: there were some keybits that Bob was unsure about 
                 whether they were 0 or 1.  "bits2drop" is a list that indicates
                 the places of these list. Bob keeps this list for Alice: she needs
                 needs to know which bits to drop from the original key sequence
                 '''     
    assert isBinary(ciphertext) == True, \
    "2nd argument must be binary"
    assert isBinary(channel_seq_bob) == True, \
    "1st argument must be binary"
    assert len(ciphertext) % block_size == 0,\
    "Check that the first input is \
     the output of encrypt().Check that the block_size was the same in encrypt()."
    assert type(block_size) == int, \
    "the second argument must be an integer"
    assert (type(threshold) == int), \
    "theshold must be an integer."
    
    
    # the length of the key
    k = int(len(ciphertext) / block_size)
    #XoR the two seqeunces and group them in blocks    
    xor_seq = [s1^s2 for s1,s2 in zip(channel_seq_bob,ciphertext)]   
    xor_seq_grouped = np.array(xor_seq).reshape(k,block_size)
    #find the hamming weight of each group
    hamming_weights = sum(xor_seq_grouped.T)
    # initialise the key estimate
    estimate_key = np.ones(k)
    # initiliase list that indicates the places for which Bob cannot make a
    # decision about the keybit. The bits of these places will be dropped for
    # the final key.
    bits2drop = []
    
    t1, t2 = threshold, (block_size - threshold)

    for i in range(k):
        if hamming_weights[i] <= t1:
            estimate_key[i] = 0
        elif hamming_weights[i] >=t2:
            estimate_key[i] = 1
        else:
            bits2drop.append(i)    
            estimate_key[i] = 3 # "3" indicates uncertainty about the key. 
                                #This keybit will be dropped after the loop ends. 
    return [int(i) for i in estimate_key], bits2drop

def genCorrSeq(length, mismatches_dec):
    '''Generates two binary sequences with a number of mismatches. 
    The positions of the mismathces are generates randomly.
    1st arg: the lenght of each sequence
    2nd arg: the percentage of mismatches between the two sequences. Write in decimal
    Output: Two binary sequences that agree in all but "no_mismatches" bits, 
    where "no_mismatches"  is the second argument.
    '''
    assert (mismatches_dec <= 1) and (mismatches_dec >= 0), \
    "mismatches_dec needs to be a decimal between 0 and 1"
    no_mismatches = int(np.round(mismatches_dec * length))
    # generate Alice's sequence 
    seq_alice = [randint(0, 1) for _ in range(length)]
    # initiate Bob's sequence
    seq_bob = [i for i in seq_alice] # "seq_bob = seq_alice" did not work for some reason 
    # pick places for the mismatches
    random_indices = sample(range(length), no_mismatches)
    # flip the bits at the previously selected positions.
    for indx in random_indices:
        seq_bob[indx] = int(seq_bob[indx]^1)

    return seq_alice, seq_bob