# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:23:42 2022

@author: cp17593
"""
import numpy as np

def is_Binary(myList):
    ''' Checks if a list (or tuple) is binary. Returns True or False.'''
    return set(myList) == {0,1}

def encrypt(key,channelSeq, blockSize=3):
    ''' Inputs: key:          the binary session key created by Alice's PRNG
                channel_seq:  the binary channel sequence at Alice
                block_size:   determines the size of the blocks that the 
                channel_seq is grouped into for encryption
        Output: returns the ciphertext with size block_size*key'''
        
    assert is_Binary(key) == True , "Key must be binary"
    assert is_Binary(channelSeq) == True , "Sequence must be binary"
    assert len(key)*blockSize <= len(channelSeq) , "The channel sequence is \
        not long enough. Inrease the length of the channel sequence, or reduce\
        the blocksize and/or the keysize."
        
    stretchKey =  np.repeat(key, blockSize) # stretches the length of the \
        # key to facilitate encyption by XoRing.     
        
    return [z[0]^z[1] for z in zip(stretchKey, channelSeq)] 