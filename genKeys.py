import scipy.io
import sys
import pandas as pd
import numpy as np
from scipy import fftpack
from matplotlib import pyplot as plt
import filters
import quantizer
from outstream import OutStream
import testsuite_bridge

def remove( listvalues, value ):
    """
    Creates new list any occurence of value.
    returns new list without value.
    """
    newlist = list()
    for avalue in listvalues:
        if( avalue != value ):
            newlist.append(avalue)
        else:
             print(avalue)
    return newlist

def validate( keybits, M ):
    """
    First breaks up keybits into shorter segments.  For each segment multiple randomness checks are performed.
    returns dictionary of test name mapping to tuple of number segments that passed the test, number of segments)
    """
    results = dict()

    # Dictionary of tests, as name -> function, avoids long if-else statement
    # Not certain if all tests return tuple of (float p-value,boolean passed)
    testFunctions = testsuite_bridge.getTestFunctions()


    for functionName in testFunctions:
        testFunction = testFunctions[functionName]
        numSegments = 0
        numPassed = 0
        i = 0
        #print( 'total length' )
        #print( len(keybits) )
        while( i + M <= len(keybits) ):
            segment = keybits[i:i+M]
            # Expected return of (float p-value,boolean passed)
            # Though not certain this is true for all test functions
            #print( "SEGMENT" )
            #print( segment )

            """
            Sometimes returns more than 2 values, Eve gets this with really bad sequences
            Can recreate with following (specifically 1 bit quantization)
            python3 analyze.py ./skyglow/Scenario2-Office-NLoS/data_eave_NLOS.mat 100000 3.0 1 0.5
            Fails with test <function RunTest.longest_one_block_test at ...>
            (0.0, False, 'Error: Not enough data to run this test')
            """
            
            returned = testFunction(segment)
            p_value = returned[0]
            passed  = returned[1]
            if( len(returned) > 2 ):
                print("TEST")
                print(testFunction)
                print("SEGMENT")
                print(segment)
                print("RETURNED")
                print(returned)
                raise IOError("PROBLEM")
                
            if( passed ):
                numPassed = numPassed + 1
            numSegments = numSegments + 1

            i = i + M

        results[functionName] = (numPassed, numSegments)

    return results

def writeKey( filename, key, limit=None ):
    # Output the key bits so can test randomness with the NIST tool
    # The key bits may have -1 as indicator of unknown but we remove when saving
    # Two formats are supported: string of '0' and '1' and a hexstring format.
    # We save using first format that supports multiple lines for easier readability
    # The test suite will reassemble all lines into one long bit string and test the first million.
    # (see ./randomness_testsuite/data/data.e and ./randomness_testsuite/teste.py)
    # 
    output = OutStream(filename)
    i = 0
    for bit in key:
        i = i + 1
        if( bit == 0 ):
            output.write( "0" )
        elif( bit == 1 ):
            output.write( "1" )
        else:
            output.write("U")
            #output.close()
            #raise Exception("Encountered invalid bit value " + str(bit))
        
        # Add new line if we have filled current line
        if( i > 0 and i % 128 == 0 ):
            output.writeln()

        # See if we have reached the limit
        if( limit is not None and i >= limit ):
            break
    output.close()


def join( elements, delimiter="" ):
    """
    Takes list elements and combines to form str with delimiter between elements.
    Same as str.join but we convert elements (so they don't have to already be str)
    returns str with str(elements[0]) + delimiter + str(elements[1]) + delimiter ...
    """
    s = ""
    delimit = len(delimiter) > 0
    for element in elements:
        s += str(element)
        if( delimit ): s.append( delimiter )
    return s

def accuracy( aliceKey, bobKey ):
    """
    Compares how well the 1 and 0 match between same length keys.
    Any other value (e.g. -1) results in a non match even if both are unknown.
    :param aliceKey: list of int values in {-1,0,1}
    :param bobKey: list of int values in {-1,0,1}
    :return: tuple (int number of 1's and 0's that matched between keys, int total compared)
    """
    correct = 0
    total   = 0
    for i in range( len(aliceKey) ):
        total = total + 1
        aliceValue = aliceKey[i]
        bobValue   = bobKey[i]
        if( aliceValue == bobValue and aliceValue == 1 ):
            correct = correct + 1
        elif( aliceValue == bobValue and aliceValue == 0 ):
            correct = correct + 1
        #elif (aliceValue == bobValue and aliceValue == -1):
        #    correct = correct + 1
    return correct, total


def getSequence(filename, window, N, var_factor, verbose):

    # a dictionary containing a few databases from matlab
    mat = scipy.io.loadmat( filename )
    rssiPairs = mat["A"]
    '''mat contains two databases: 
    mat["A"] - rssi measurments
    mat["T"] - don't know (maybe the time of the measurement)
    '''

    # extracts alice and bob databases
    i = 0
    rssiAlice = list()
    rssiBob   = list()
    for rssiPair in rssiPairs:
        #if(i > 2048 + 1): break
        # Add to series for plotting
        rssiAlice.append( rssiPair[0] )
        rssiBob.append(   rssiPair[1] )
        i = i + 1


    # filters the data, we can use different filter methods
    params = {'window': int(window), "verbose": bool(verbose)}
    alice_filtered = filters.nearest_neighbor(rssiAlice, params)
    bob_filtered = filters.nearest_neighbor(rssiBob, params)

    df_filtered = pd.DataFrame(alice_filtered, columns=['filtered alice'])
    df_filtered['filtered bob'] = bob_filtered
    var_alice = df_filtered['filtered alice'].var()
    var_bob = df_filtered['filtered bob'].var()
    limit = var_factor * (var_alice + var_bob)/2
    df_filtered.plot(title='window' + str(window) + ' limit ' + str(limit))
    plt.plot([0,  100499], [limit, limit], label='limit everything above it is 11')
    plt.plot([0, 100499], [-limit, -limit], label='limit everything above it is 00')
    plt.legend()
    plt.tight_layout()
    plt.show()


    # returns quantized sequence
    alice_key = quantizer.uniform(alice_filtered, N, limit, verbose=True)
    bob_key = quantizer.uniform(bob_filtered, N, limit, verbose=True)
    # writeKey( "aliceKeyB.txt", alice_key )

    '''

    # See how well Alice and Bob agreed
    correct, total = accuracy( alice_key, bob_key )
    percentAccurate = correct / total
    print( f"Alice and Bob agreement: {percentAccurate:.4f}"  )
    writeKey("aliceKey.txt", alice_key, 128)
    writeKey("bobKey.txt",     bob_key, 128)

    '''
    # Remove all the unknown bits from the sequences
    aliceKey = remove(alice_key, -1.0)
    bobKey   = remove(bob_key,   -1.0)


    print(len(aliceKey))
    print(len(alice_key))
    print('aliceKey==alice_key ', aliceKey==alice_key)


    # Convert into str with all bits contiguously together (no spaces, for passing to testsuite)
    aliceKeyStr = join(alice_key)
    bobKeyStr   = join(bob_key)
    
    

    # Use the testsuite to determine if the key is sufficiently random.
    

    # This is a critical parameter for Test 2.02
    '''    
    I think this code tests their KG

    M = 128 # This agrees with the paper, they generated 128 bit keys

    print('Alice Results')
    results = validate(alice_key, M)
    for testName in results:
        numPassed, numSegments = results[testName]
        percentage = numPassed / numSegments
        print(f"passed {numPassed} / {numSegments} = {percentage:.2f}: {testName}")

    print('Bob Results')
    results = validate(bob_key, M)
    for testName in results:
        numPassed, numSegments = results[testName]
        percentage = numPassed / numSegments
        print(f"passed {numPassed} / {numSegments} = {percentage:.2f}: {testName}")'''

    return aliceKey, bobKey
