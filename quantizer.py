import math


def uniform( signal, N, limit, midrise=True, verbose=False ):
    """
    Takes signal with values assumed to be centered around zero (i.e. mean is roughly 0.0)
    and returns list N x length of the signal.  Mid-rise takes the floor while mid-tread rounds.
    :param signal:
    :param N: bits per sample
    :param limit: max_value = limit, min_value = -limit
    :return:
    """

    '''I reckon that limit is the quantization limit
    it depneds on the filtered data'''




    '''two different ways to quantize the data mid_rise and 
    mid_tread give the bourdries to convert to binary. for mid_rise see 
    example below:
    # The quant_rise_ind are around zero
    # Need to get positive index counting from min value (seems to be convention)
    # However, need to use Gray coding, will help improve key agreement
    # quant_rise_ind  offset_ind  bit_pattern
    # -4   0   000
    # -3   1   001
    # -2   2   010
    # -1   3   011
    #  0   4   100
    #  1   5   101
    #  2   6   110
    #  3   7   111'''
    if(midrise):
        quant_ind, quant_rec = mid_rise( signal, N, limit )
    else:
        quant_ind, quant_rec = mid_tread( signal, N, limit )



    '''Converts index value into one's complement.  For example, bits=3, -2 becomes [1,1,0].
    The list is returned in big-endian order, e.f. bits=4, 7 becomes [0,1,1,1].
    The code below quantizes the data'''
    index2bitlist = dict()
    offset = 2**(N-1)
    for i in range(2**N):
        bitstring = index2binary(i, N)
        #bitstring = index2gray(i, N)
        index2bitlist[i - offset] = bitstring

    # Debugging# not sure what it does
    #histogram(quant_ind, index2bitlist, verbose=verbose)

    # Convert to Gray code so only one bit error between adjacent levels
    

    if(verbose):
        print("MAPPING")
        print(index2bitlist)

    # The index values are lower bits of the index
    # Also gives us chance to convert from nparray of floats into python list of ints
    key_series = list()
    for index in quant_ind:
        bitlist = index2bitlist[index]
        key_series = key_series + bitlist
    
    # Sanity check
    input_length = len(signal)
    expected_output_length = input_length * N
    output_length = len(key_series)
    if( expected_output_length != output_length ):
        raise RuntimeError(f"Expected length {expected_output_length} but got {output_length}")

    return key_series



def index2binary(value, bits):
    """
    Converts index value into one's complement.  For example, bits=3, -2 becomes [1,1,0].
    The list is returned in big-endian order, e.f. bits=4, 7 becomes [0,1,1,1]
    :param value:
    :param bits:
    :return:
    """
    bitlist = list() # in least significant bit order, easier to code
    i = 0
    while(i < bits):
        lsb = value & 0x01
        bitlist.append( lsb )
        value = value >> 1
        i = i + 1
    bitlist.reverse()  # make most significant bit order, easier to debug imho
    return bitlist


def index2gray(value, bits):
    """
    Converts index value into one's complement then into a Gray code.
    :param value:
    :param bits:
    :return:
    """
    # https://www.gaussianwaves.com/2012/10/natural-binary-codes-and-gray-codes/
    bitlist = index2binary( value, bits )
    graycodes = list()
    graycodes.append( bitlist[0] )
    for i in range(1, bits):
        curr = bitlist[i]
        prev = bitlist[i-1]
        graycodes.append( curr ^ prev )
    return graycodes


def histogram( indexes, index2bitlist, verbose=False):
    counts = dict()
    for k in indexes:
        if (k not in counts):
            counts[k] = 0
        count = counts[k]
        count = count + 1
        counts[k] = count
    if( verbose ):
        print("Quantize Histogram")
        total_count = 0
        # Count lowest index to highest, for example
        # seems to be normal approach
        # Index Bits
        #   1 -> 11
        #   0 -> 10
        #  -1 -> 01
        #  -2 -> 00
        num_indexes = len(counts.keys())
        N = math.ceil( math.log(num_indexes, 2.0) )
        #print(f"histogram derived {N}  num_indexes {num_indexes}")
        for findex in sorted(counts.keys()):
            count = counts[findex]
            total_count += count # sanity check
            bitlist = index2bitlist[findex]
            print(f"  mapped {findex} {bitlist} -> {count}")
            #print(f"  mapped {findex} -> {count}")
            
        print(f"total samples {total_count}")
    return counts


def mid_rise( signal, N, limit ):
    """
    Takes the signal and quantized into 2**N levels within interval [-limit,+limit).
    See https://en.wikipedia.org/wiki/Quantization_(signal_processing)
    See https://www.tutorialspoint.com/digital_communication/digital_communication_quantization.htm
    Returns two lists, the index values and the quantized signal.
    :param signal:
    :param N:
    :param limit:
    :return:
    """
    max_value = limit
    min_value = -limit
    step_size = (max_value - min_value) / (2 ** N)


    ################################
    # Mid-rise Encode/Decode
    ################################
    # quant_rise_ind = (np.floor(sinewave / stepsize) + (1 / 2)) * stepsize
    epsilon = 0.0001  # for four levels indexes [i0=min, i1, i2, i3=max)
    quant_rise_ind = list()
    quant_rise_rec = list()
    for value in signal:
        # threshold to stay in limits of index
        if (value < min_value):
            value = min_value
        if (value >= max_value):
            # critically avoids extra index for max_value
            value = max_value - epsilon
        k = math.floor(value / step_size)
        # Create reconstructed quantized value
        value_rec = (k + (1 / 2)) * step_size
        quant_rise_ind.append(k)
        quant_rise_rec.append(value_rec)
    return quant_rise_ind, quant_rise_rec

def mid_tread( signal, N, limit ):
    """
    Takes the signal and quantized into 2**N levels within innterval [-limit,+limit).
    See https://en.wikipedia.org/wiki/Quantization_(signal_processing)
    See https://www.tutorialspoint.com/digital_communication/digital_communication_quantization.htm
    Returns two lists, the index values and the quantized signal.
    :param signal:
    :param N:
    :param limit:
    :return:
    """
    max_value = limit
    min_value = -limit
    step_size = (max_value - min_value) / (2 ** N)

    #
    # Ok, we have to get rid of one of the levels
    # Actual mid-tread will have 2 levels missing
    # thus leaving one of the mappings vacant.
    # e.g. N=3 will only have 7 mappings
    #          we have 9, so just need to get rid of one
    # We opt to remove one of the mappings
    # Chose the next to max value interval, merged with max value
    #

    ################################
    # Mid-tread Encode/Decode
    ################################
    # quant_tread_ind = np.floor(sinewave / stepsize + (1 / 2)) * stepsize
    quant_tread_ind = list()
    quant_tread_rec = list()
    for value in signal:
        # threshold to stay in limits of index
        if (value < min_value):
            value = min_value
        if (value > max_value - step_size):
            value = max_value - step_size
        # k = math.floor(value / stepsize + (1 / 2)) # effectively round
        k = round(value / step_size)
        # Create reconstructed quantized value
        value_rec = k * step_size
        quant_tread_ind.append(k)
        quant_tread_rec.append(value_rec)
    return quant_tread_ind, quant_tread_rec


# def dead_zone(signal, N, limit):

#     max_value = limit
#     min_value = -limit
#     step_size = (max_value - min_value) / (2 ** N)

#     quant_tread_ind = list()
#     quant_tread_rec = list()
#     for value in signal:


