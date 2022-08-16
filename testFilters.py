from asyncio import streams
from cmath import log
from logging import LoggerAdapter
import queue
import scipy.io
import sys
import pandas as pd
import numpy as np
from scipy import fftpack
from matplotlib import pyplot as plt
import quantizer
from outstream import OutStream
from filters_test import *
from SK_functions import *
import multiprocessing 
import time 
from testsuite_bridge import getTestFunctions


class KeyGenFilter():

    def __init__(self):
        self.keydata = pd.DataFrame(columns=['filter', 'window', 'alpha', 'lag', 'alphaLP', 'alphaHP', 'no mismatchess', 
            'Key Lenght', 'Key Sattus', 'Key bit Mismatches', 'Key bit Matches', 'key bit mismatches %', 
            'Seq bit Mismatches', 'Seq bit Matches', 'Seq bit mismatches %'])

        

    def remove(self,  listvalues, value ):
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



    def validate(self, keybits, M ):
        """
        First breaks up keybits into shorter segments.  For each segment multiple randomness checks are performed.
        returns dictionary of test name mapping to tuple of number segments that passed the test, number of segments)
        """
        results = dict()

        # Dictionary of tests, as name -> function, avoids long if-else statement
        # Not certain if all tests return tuple of (float p-value,boolean passed)
        testFunctions = getTestFunctions()


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


    def join(self, elements, delimiter="" ):
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

    def show_filtered_data(self, alice_filtered, bob_filtered, title, N, var_factor):

        df_filtered = pd.DataFrame(alice_filtered, columns=['filtered alice'])
        df_filtered['filtered bob'] = bob_filtered
        var_alice = df_filtered['filtered alice'].var()
        var_bob = df_filtered['filtered bob'].var()
        limit = var_factor * (var_alice + var_bob)/2
        title = f'{title}{str(limit)}'

        # df_filtered.plot(title=title)
        # step_size = (limit + limit) / (2 ** N)
        # getbinary = lambda x, n: format(x, 'b').zfill(n)
        # plt.plot([0, 5000], [-limit, -limit], label=f'limit, values below are set to {"0"*N}, above is {"0"*N}')
        # for multi in range(2 ** N):
        #     if int(multi)!=0:
        #         plt.plot([0,  5000], [-limit + multi*step_size, -limit + multi*step_size],
        #         label=f'above is {str(getbinary(multi, N))}')
    
        # plt.plot([0,  5000], [limit, limit], label=f'limit, values above are set to {"1"*N}')
        # plt.legend()
        # plt.tight_layout()
        # plt.savefig(f'plots/{title}.png')

        return limit



    def testMiss(self, seq_alice, seq_bob, printIt=False):
        i = 0
        missmatches = []
        ok = []
        for bit_alice, bit_bob in zip(seq_alice, seq_bob):
            if bit_alice!=bit_bob:
                missmatches.append((i, bit_alice, bit_bob))
            else:
                ok.append((i, bit_alice, bit_bob))
            i+=1

        if printIt:
            print(missmatches)

        return len(missmatches), len(ok), len(missmatches)/(len(missmatches)+len(ok))


    

    def checkQuantize(self, key):
        KeyRemove = self.remove(key, -1.0)

        if KeyRemove==key:
            return None
        else:
            print('A grave mistake has happened key remove is different than key')
            return KeyRemove




    def performkeyGen(self, seq_alice, seq_bob, block_size, length_of_key, threshold):
        SeqMismatches, SeqMatches, SeqProc_mismatched  = self.testMiss(seq_alice, seq_bob)
        np_seq_alice = np.array(seq_alice)
        np_seq_bob = np.array(seq_bob)
        np_miss_array = np.where(np_seq_alice!=seq_bob)


        key_alice = keyAlice(length_of_key) 
        
        #Alice encrypts the key.
        cipher = encrypt(key_alice,seq_alice, block_size)
            
        # Bob decrypts Alice's cipher
        key_bob, bits2drop = decrypt(seq_bob, cipher, threshold ,block_size)
        
        # Ideally "key_bob" consists of 0s and 1s. Any 3s  in key_bob indicates
        # that Bob does not know the binary values at those positions. All 3s must be
        # dropped. Bob needs to communicates the positions of 3s to Alice. 
        # This information is reserved in "bits2drop". The following two lines drop
        # those bits from both key-sequences at Alice and Bob.
        [key_alice.pop(b) for b in reversed(bits2drop)]
        [key_bob.pop(b) for b in reversed(bits2drop)]


        KeyMismatches, KeyMatches, KeyProc_mismatched = self.testMiss(key_alice, key_bob)
     
            
    
        number_mismatches = sum([i^j for i,j in zip(key_alice,key_bob)])
        print(number_mismatches)


        return number_mismatches, len(key_alice), key_alice == key_bob, KeyMismatches, \
            KeyMatches, KeyProc_mismatched, SeqMismatches, SeqMatches, SeqProc_mismatched 



    def nearest_neighbour_pipe(self, rssiAlice, rssiBob , window, N, var_factor, column, block_size, length_of_key, threshold):
        


        # filters the data, we can use different filter methods
        params = {'window': int(window), "verbose": bool(False)}
        alice_filtered = nearest_neighbor(rssiAlice, params)
        bob_filtered = nearest_neighbor(rssiBob, params)

        title = 'window ' + str(window) + ' limit '
        if window:#'' in [50]:
            limit = self.show_filtered_data(alice_filtered, bob_filtered, title, N, var_factor)
            if limit==0:
    
                return

            alice_key = quantizer.uniform(alice_filtered, N, limit, verbose=False)
            bob_key = quantizer.uniform(bob_filtered, N, limit, verbose=False)
        if window in [50, 60]:
            aliceStr = self.join(alice_key)
            bobStr = self.join(bob_key)

            print('Alice Results')
            results = self.validate(aliceStr, 128)
            for testName in results:
                numPassed, numSegments = results[testName]
                percentage = numPassed / numSegments
                print(f"passed {numPassed} / {numSegments} = {percentage:.2f}: {testName}")

            print('Bob Results')
            results = self.validate(bobStr, 128)
            for testName in results:
                numPassed, numSegments = results[testName]
                percentage = numPassed / numSegments
                print(f"passed {numPassed} / {numSegments} = {percentage:.2f}: {testName}")



            self.checkQuantize(alice_key)
            self.checkQuantize(bob_key)
            

            number_mismatches, KeyLen, KeyStatus, KeyMismatches, KeyMatches, \
                KeyProc_mismatched, SeqMismatches, SeqMatches, \
                    SeqProc_mismatched = self.performkeyGen(
                    alice_key, bob_key, block_size, length_of_key, threshold)

            self.keydata.loc[len(self.keydata.index)] = [column, window, '    -    ', '    -    ', '    -    ', '    -    ', number_mismatches, 
                KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
                SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]
        else:
            return


        # return [column, window, '    -    ', '    -    ', '    -    ', '    -    ', number_mismatches, 
        #     KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
        #     SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]




    def lowpass_lagged_pipe(self, rssiAlice, rssiBob , lag, alpha, N, var_factor, column, block_size, length_of_key, threshold):


        params = {'alpha':alpha, 'verbose':False, 'lag':lag}
        
        alice_filtered = lowpass_lagged(rssiAlice, params)
        bob_filtered = lowpass_lagged(rssiBob, params)

        title= 'lowpass lagged, lag: ' +str(lag)+ ' alpha ' + str(alpha) + ' '
        params = (alpha, lag)
        if params:# in [(0, 7), (0, 25), (0.2, 2), (0.3, 80), (0.5, 100), (0.8, 20), (0.9, 300)]:
            limit = self.show_filtered_data(alice_filtered, bob_filtered, title, N, var_factor)
            if limit==0:

                return


            alice_key = quantizer.uniform(alice_filtered, N, limit)
            bob_key = quantizer.uniform(bob_filtered, N, limit)


            # self.remove all the unknown bits from the sequences
            self.checkQuantize(alice_key)
            self.checkQuantize(bob_key)


            number_mismatches, KeyLen, KeyStatus, KeyMismatches, KeyMatches, \
                KeyProc_mismatched, SeqMismatches, SeqMatches, \
                    SeqProc_mismatched = self.performkeyGen(
                    alice_key, bob_key, block_size, length_of_key, threshold)
            self.keydata.loc[len(self.keydata.index)] = [column, '    -    ', alpha, lag, '    -    ', '    -    ', number_mismatches, 
                KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
                SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]
        else:
            return
        # return [column, '    -    ', alpha, lag, '    -    ', '    -    ', number_mismatches, 
        #     KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
        #     SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]






    def ewma_pipe(self, rssiAlice, rssiBob , alpha, N, var_factor, column, block_size, length_of_key, threshold):

        alice_filtered = ewma(rssiAlice, alpha)
        bob_filtered = ewma(rssiBob, alpha)

        title = 'ewma - alpha '+str(alpha) + ' '
        limit = self.show_filtered_data(alice_filtered, bob_filtered, title, N, var_factor)
        if limit==0:

            return


        alice_key = quantizer.uniform(alice_filtered, N, limit, verbose=False)
        bob_key = quantizer.uniform(bob_filtered, N, limit, verbose=False)


        # self.remove all the unknown bits from the sequences
        self.checkQuantize(alice_key)
        self.checkQuantize(bob_key)

        

        number_mismatches, KeyLen, KeyStatus, KeyMismatches, KeyMatches, \
            KeyProc_mismatched, SeqMismatches, SeqMatches, \
                SeqProc_mismatched = self.performkeyGen(
                alice_key, bob_key, block_size, length_of_key, threshold)

        self.keydata.loc[len(self.keydata.index)] = [column, '    -    ', alpha, '    -    ', '    -    ', '    -    ', number_mismatches, 
        KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
        SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]

        # return [column, '    -    ', alpha, '    -    ', '    -    ', '    -    ', number_mismatches, 
        #     KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
        #     SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]





    def bandpassHPLP_pipe(self, rssiAlice, rssiBob , alphaLP, alphaHP, N, var_factor, column, block_size, length_of_key, threshold):

        alice_filtered = bandpassHPLP(rssiAlice, alphaLP, alphaHP)
        bob_filtered = bandpassHPLP(rssiBob, alphaLP, alphaHP)

        title = 'bandpassHPLP - alphaLP: '+str(alphaLP) + ' alphaHP: ' + str(alphaHP) + ' '
        params = (alphaLP, alphaHP)
        if params:# in [(0.2, 0.9), (0.5, 0.1), (0.7, 0.1)]:
            limit = self.show_filtered_data(alice_filtered, bob_filtered, title, N, var_factor)
            if limit==0:

                return

            alice_key = quantizer.uniform(alice_filtered, N, limit)
            bob_key = quantizer.uniform(bob_filtered, N, limit)


            # self.remove all the unknown bits from the sequences
            self.checkQuantize(alice_key)
            self.checkQuantize(bob_key)

            

            number_mismatches, KeyLen, KeyStatus, KeyMismatches, KeyMatches, \
                KeyProc_mismatched, SeqMismatches, SeqMatches, \
                    SeqProc_mismatched = self.performkeyGen(
                    alice_key, bob_key, block_size, length_of_key, threshold)

            self.keydata.loc[len(self.keydata.index)] = [column, '    -    ', '    -    ', '    -    ', alphaLP, alphaHP, number_mismatches, 
            KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
            SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]
        else:
            return

        # return [column, '    -    ', '    -    ', '    -    ', alphaLP, alphaHP, number_mismatches, 
        #     KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
        #     SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]



    
    def bandpassLPHP_pipe(self, rssiAlice, rssiBob , alphaLP, alphaHP, N, var_factor, column, block_size, length_of_key, threshold):

        alice_filtered = bandpassLPHP(rssiAlice, alphaLP, alphaHP)
        bob_filtered = bandpassLPHP(rssiBob, alphaLP, alphaHP)

        title = 'bandpassHPLP - alphaLP: '+str(alphaLP) + ' alphaHP: ' + str(alphaHP) + ' '
        params = (alphaLP, alphaHP)
        if params:# in [(0.2, 0.9), (0.7, 0.2), (0.8, 0.3), (0.9, 0.3)]:
            limit = self.show_filtered_data(alice_filtered, bob_filtered, title, N, var_factor)
            if limit==0:

                return


            alice_key = quantizer.uniform(alice_filtered, N, limit, verbose=False)
            bob_key = quantizer.uniform(bob_filtered, N, limit, verbose=False)


            # self.remove all the unknown bits from the sequences
            self.checkQuantize(alice_key)
            self.checkQuantize(bob_key)

        
            number_mismatches, KeyLen, KeyStatus, KeyMismatches, KeyMatches, \
                KeyProc_mismatched, SeqMismatches, SeqMatches, \
                    SeqProc_mismatched = self.performkeyGen(
                    alice_key, bob_key, block_size, length_of_key, threshold)

            self.keydata.loc[len(self.keydata.index)] = [column, '    -    ', '    -    ', '    -    ', alphaLP, alphaHP, number_mismatches, 
            KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
            SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]
            
        # return  [column, '    -    ', '    -    ', '    -    ', alphaLP, alphaHP, number_mismatches, 
        #     KeyLen, KeyStatus, KeyMismatches, KeyMatches, round(KeyProc_mismatched, 4), 
        #     SeqMismatches, SeqMatches, round(SeqProc_mismatched, 4)]









class RunPipeline():

    def __init__(self, filename, N, ver_factor, block_size, length_of_key, threshold):
        self.KG_filter = KeyGenFilter()
        self.N = N
        self.ver_factor = ver_factor
        self.block_size = block_size
        self.length_of_key = length_of_key
        self.threshold =threshold
        self.get_file(filename)
        self.nearest = None


    def run_pipeline_multicore(self):
    
        nearest = multiprocessing.Process(target=self.run_nearest_neighbor).start()
        lagged = multiprocessing.Process(target=self.run_lowpass_lagged).start()
        hplp = multiprocessing.Process(target=self.run_bandpassHPLP).start()
        lphp = multiprocessing.Process(target=self.run_bandpassLPHP).start()

        return nearest, lagged, hplp, lphp

    def run_pipeline(self):
    
        self.run_nearest_neighbor()
        # self.run_lowpass_lagged()
        # self.run_bandpassHPLP()
        # self.run_bandpassLPHP()



    def get_file(self, filename):
        mat = scipy.io.loadmat( filename )
        rssiPairs = mat["A"]

        # extracts alice and bob databases
        i = 0
        alice = list()
        bob   = list()
        for rssiPair in rssiPairs:
            #if(i > 2048 + 1): break
            # Add to series for plotting
            alice.append( rssiPair[0] )
            bob.append(   rssiPair[1] )
            i = i + 1
        self.rssiAlice = alice[:5000]
        self.rssiBob = bob[:5000]


    def run_nearest_neighbor(self):
        windows=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, ]
        result = []
        for window in windows:
            result.append(self.KG_filter.nearest_neighbour_pipe(self.rssiAlice, self.rssiBob, window, self.N, self.ver_factor,
             'nearest neighbour', self.block_size, self.length_of_key, self.threshold))

        print('nearest neighbour finished running')
        # queue.put(result)

    def run_lowpass_lagged(self):
        alphaArray = np.linspace(0, 1, 11)
        lagArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300]
        result = []
        for alpha in alphaArray:
            for lag in lagArray:
                result.append(self.KG_filter.lowpass_lagged_pipe(self.rssiAlice, self.rssiBob, lag, alpha, self.N, self.ver_factor,
                 'lowpass lagged', self.block_size, self.length_of_key, self.threshold))


        print('lowpass lagged finished running')
        # queue.put(result)
        

    def run_ewma(self):
        alphaArray = np.linspace(0, 1, 11)
        for alpha in alphaArray:
            self.KG_filter.ewma_pipe(self.rssiAlice, self.rssiBob, alpha, self.N, self.ver_factor,
             'ewma', self.block_size, self.length_of_key, self.threshold)
        print('ewma finished running')


    def run_bandpassHPLP(self):
        result =[]
        alphaArray = np.linspace(0, 1, 11)
        for alphaLP in alphaArray:
            for alphaHP in alphaArray:
                result.append(self.KG_filter.bandpassHPLP_pipe(self.rssiAlice, self.rssiBob, alphaLP, alphaHP, self.N, self.ver_factor,
                 'bandpassHPLP', self.block_size, self.length_of_key, self.threshold))
        # queue.put(result)
        print('bandpassHPLP finished running')
        


    def run_bandpassLPHP(self):
        alphaArray = np.linspace(0, 1, 11)
        result = []
        for alphaLP in alphaArray:
            for alphaHP in alphaArray:
                result.append(self.KG_filter.bandpassLPHP_pipe(self.rssiAlice, self.rssiBob, alphaLP, alphaHP, self.N, self.ver_factor,
                'bandpassLPHP', self.block_size, self.length_of_key, self.threshold))
        print('bandpassLPHP finished running')
        # queue.put(result)


        
if __name__ == '__main__':
    '''

    EXAMPLE TO RUN:
        python3 testFilters.py data3_upto5.mat 2 2 6 300 1 



    inputs:
    filename = the name of the file that contains the data
    var_factor = the mupliplier of variance to set the limit to quantize
    N = number of bits to quantize to
    block_size = length of the key stretch
    length_of_key = lenght of the key
    threshold = 

    outputs:
    filters.csv and filters.html, whatever is more convenient

    the program compares resustls for different sets of parameters accros different 
    filtering algorithms: NEAREST NEIGHBOURS, lowpass lagged, 
    ewma (exponantionaly weighted movinbg average, probably doesn't work), bandpassHPLP,
    bandpassLPHP.
    Since there are about 500 iterations no grahs are made


    the program extracts only 20'000 datapoints (method get_file; class RunPipeline)
    to speed up the process

    the values that are printed are the number of mismatches between alice and bob keys, 
    the value is printed out just to see the speed of the program


    ON MY MACHINE THE PROGRAM RUNSS FOR 12 MINUTES  
    working on spliting the computations to different processor cores
    '''

    filename = str(sys.argv[1])
    var_factor = float(sys.argv[3])
    N = int(sys.argv[2])
    block_size = int(sys.argv[4])
    length_of_key = int(sys.argv[5])
    threshold = int(sys.argv[6])


    print(f'filename={filename}    N={N}    var_factor={var_factor}    block_size={block_size}    length_of_key={length_of_key}     threshold={threshold}')


    pipeline = RunPipeline(filename, N, var_factor, block_size, length_of_key, threshold)

    start = time.perf_counter()
    pipeline.run_pipeline()
    #nearest, lagged, hplp, lphp = pipeline.run_pipeline_multicore()
    #print(nearest, lagged, hplp, lphp)
    # pool = multiprocessing.Pool(processes=4)
    # result = [pipeline.run_nearest_neighbor, pipeline.run_bandpassHPLP, pipeline.run_bandpassLPHP,pipeline.run_lowpass_lagged]
    # result_nearest  = pool.map(result, range(4) )

    # print('result ', result)

    # nearest.start()
    # lagged.start()
    # hplp.start()
    # lphp.start()
    #nearest.join()
    #lagged.join()
    #hplp.join()
    #lphp.join()


    




    # result = nearest.exitcode + lagged.exitcode + hplp.exitcode + lphp.exitcode
    # print('result ', nearest.result() )
    # print('result ', lagged.result())
    # print('result ', hplp.result())
    # print('result ', lphp.result())
    
    
    
    stop = time.perf_counter()
    print('the time elapsed', stop-start)
    

    # calling the populated dataframe
    dataframe = pipeline.KG_filter.keydata
    # writing to csv
    dataframe.to_csv(f'filters_var-{var_factor}_N-{N}_bs-{block_size}_kl-{length_of_key}_thr-{threshold}.csv', sep='\t')

    # writing a file to html
    html = dataframe.to_html()

    #write html to file
    text_file = open(f'filters_var-{var_factor}_N-{N}_bs-{block_size}_kl-{length_of_key}_thr-{threshold}', "w")
    text_file.write(html)
    text_file.close()
    
