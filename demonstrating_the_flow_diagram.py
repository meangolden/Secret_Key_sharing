# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 12:42:56 2022

link:
flow diagram alice: 
flow diagram bob:

@author: cp17593
"""

import numpy as np
import random
from SK_functions import genCorrSeq


# Give Alice and Bob two correlated sequences.#################################
# In the paper, these are referred to as the "channel sequences".
# In reality, these sequences are derived through measurements of the reciprocal
# reciprocal RF channel between Alice and Bob, e.g. RSS measusements.    
mismatches_dec = 0.2              
alice_seq, bob_seq = genCorrSeq(int(1e5), mismatches_dec)

# Shuffle the sequences. Use the same permutation.#############################
# Why? In practice, Alice's and Bob's channel will have runs of missmathces.
# We need the mismatches spread out. 
same_seed = 42 # a fixed value known by both Alice and Bob. Agreed a priori.
              # it can be any number. 
# Alice permutes:
np.random.seed(same_seed)
print(np.random.permutation(alice_seq))                                  
#Bob does the same thing:                               
np.random.seed(same_seed)
print(np.random.permutation(bob_seq))

# Choosing parameters for encryption ##########################################
# This is the first subroutin of the flow diagrams "flow_main_alice.pdf" and
# "flow_main_alice.pdf". This subroutine has two steps for both parties:

# 2. Use the look up table and set the parameters for encoding/decoding.



 