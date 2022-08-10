"""
Front end to the NIST randomness test suite.
See https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=906762.
There are 15 different tests (though not all may apply).
This assumes the submodule randomness_testsuite has been clones in this directory.
    git clone https://github.com/stevenang/randomness_testsuite
"""

import os
import sys

# Add the modules from randomness_testsuite
sys.path.append("./randomness_testsuite")
from FrequencyTest import FrequencyTest
from RunTest import RunTest
from Matrix import Matrix
from Spectral import SpectralTest
from TemplateMatching import TemplateMatching
from Universal import Universal
from Complexity import ComplexityTest
from Serial import Serial
from ApproximateEntropy import ApproximateEntropy
from CumulativeSum import CumulativeSums
from RandomExcursions import RandomExcursions


def cumsumForward( binary_data ):
    return CumulativeSums.cumulative_sums_test(binary_data[:1000000], 0)

def cumsumBackward( binary_data ):
    return CumulativeSums.cumulative_sums_test(binary_data[:1000000], 1)

def getTestFunctions():
    """
    Gets mapping of test names to functions.  Each function takes one str parameter of '01010...' values.
    Each function in the dictionary when called returns (float p-value,boolean passed).
    Thus, each function is of the form
        (float p-value,boolean passed) = function( str binary_data )
    return dict mapping str testName to test function
    """
    functions = dict()
    functions["2.01. Frequency Test"]        = FrequencyTest.monobit_test
    functions["2.02. Block Frequency Test"]  = FrequencyTest.block_frequency
    functions["2.03. Run Test"]              = RunTest.run_test
    functions["2.04. Run Test (Longest Run of Ones)"] = RunTest.longest_one_block_test

    #functions["2.11. Serial Test"] = Serial.serial_test
    
    #Temporary comment out because giving an error to investigate
    #functions["2.12. Approximate Entropy Test"] = ApproximateEntropy.approximate_entropy_test

    functions["2.13. Cumulative Sums (Forward)"] = cumsumForward
    functions["2.13. Cumulative Sums (Backward)"] = cumsumBackward



    return functions

def test_2_02( binary_data ):
    """
    Performs test 2.02 on the 0-1 str binary_data.
    returns True if determined Random, False determined Non-Random
    """
    # The p_value threshold is hardcoded as 0.01
    p_value, passed = FrequencyTest.block_frequency(binary_data[:1000000])
    #print( f"p_value={p_value}" )
    return p_value, passed


def evaluate( binary_data ):
    """
    binary_data str of 0's and 1's with no spaces, e.g. '111101001101110'
    See Chapter 2 in the NIST guide 
    """
    print('The statistical test of the Binary Expansion of e')
    print('2.01. Frequency Test:\t\t\t\t\t\t\t\t', FrequencyTest.monobit_test(binary_data[:1000000]))
    print('2.02. Block Frequency Test:\t\t\t\t\t\t\t', FrequencyTest.block_frequency(binary_data[:1000000]))
    print('2.03. Run Test:\t\t\t\t\t\t\t\t\t\t', RunTest.run_test(binary_data[:1000000]))
    print('2.04. Run Test (Longest Run of Ones): \t\t\t\t', RunTest.longest_one_block_test(binary_data[:1000000]))
    print('2.05. Binary Matrix Rank Test:\t\t\t\t\t\t', Matrix.binary_matrix_rank_text(binary_data[:1000000]))
    print('2.06. Discrete Fourier Transform (Spectral) Test:\t', SpectralTest.spectral_test(binary_data[:1000000]))
    print('2.07. Non-overlapping Template Matching Test:\t\t', TemplateMatching.non_overlapping_test(binary_data[:1000000], '000000001'))
    print('2.08. Overlappong Template Matching Test: \t\t\t', TemplateMatching.overlapping_patterns(binary_data[:1000000]))
    print('2.09. Universal Statistical Test:\t\t\t\t\t', Universal.statistical_test(binary_data[:1000000]))
    print('2.10. Linear Complexity Test:\t\t\t\t\t\t', ComplexityTest.linear_complexity_test(binary_data[:1000000]))
    print('2.11. Serial Test:\t\t\t\t\t\t\t\t\t', Serial.serial_test(binary_data[:1000000]))
    print('2.12. Approximate Entropy Test:\t\t\t\t\t\t', ApproximateEntropy.approximate_entropy_test(binary_data[:1000000]))
    print('2.13. Cumulative Sums (Forward):\t\t\t\t\t', CumulativeSums.cumulative_sums_test(binary_data[:1000000], 0))
    print('2.13. Cumulative Sums (Backward):\t\t\t\t\t', CumulativeSums.cumulative_sums_test(binary_data[:1000000], 1))
    result = RandomExcursions.random_excursions_test(binary_data[:1000000])
    print('2.14. Random Excursion Test:')
    print('\t\t STATE \t\t\t xObs \t\t\t\t P-Value \t\t\t Conclusion')

    for item in result:
        print('\t\t', repr(item[0]).rjust(4), '\t\t', item[2], '\t\t', repr(item[3]).ljust(14), '\t\t',
              (item[4] >= 0.01))

    result = RandomExcursions.variant_test(binary_data[:1000000])

    print('2.15. Random Excursion Variant Test:\t\t\t\t\t\t')
    print('\t\t STATE \t\t COUNTS \t\t\t P-Value \t\t Conclusion')
    for item in result:
        print('\t\t', repr(item[0]).rjust(4), '\t\t', item[2], '\t\t', repr(item[3]).ljust(14), '\t\t',
              (item[4] >= 0.01))

def main():
    # Reads in file, makes one long str and calls evaluate.
    if( len(sys.argv) != 2 ):
        print("Usage: <binary string filename>")
        print("Example: /home/user/Desktop/skyglow/Scenario2-Office-LoS/aliceKey.txt")
        return
    filename = sys.argv[1]

    # Open Data File and read the binary data of e
    #data_path = os.path.join(os.getcwd(), 'data', 'data.e')
    handle = open(filename)
    data_list = []

    for line in handle:
        data_list.append(line.strip().rstrip())

    binary_data = ''.join(data_list)
    evaluate( binary_data )
    

if __name__ == '__main__':
    main()


