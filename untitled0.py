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




#parameters -WHAT Alice and Bob 
sameSeed = 42 # a fixed value known by both Alice and Bob. Agreed a priori.
              # it can be any number 

# Give Alice and Bob two correlated sequences. In the paper, these are referred
# to as the "channel sequences". In reality, these sequences are derived through
# measurements of the reciprocal RF channel between Alice and Bob, e.g. RSS 
# measusements.    
aliceSeq, bobSeq = genCorrSeq(length=1e^4, mismatches_dec=0.2)


 = [1,1,1,0,0,0,1,1,1,0,0,0] 
bobSeq =   [1,1,1,0,0,0,1,1,1,0,0,0] #in reality this sequence may be
                                     # a bit different to Alice's
                                    
#What alice do in her end:
np.random.seed(mySeed)
print(np.random.permutation(aliceSeq))                                    
                                    
                                    
#Bob does the same thing:
                                    
np.random.seed(sameSeed)
print(np.random.permutation(bobSeq))                                   