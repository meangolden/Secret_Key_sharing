from scipy.signal import butter, lfilter
import pandas as pd
import matplotlib.pyplot as plt



'''There are many filters James creeated everyone returns filtered series. 
For now I will add only the "nearest neighbour" filter'''


# somting that might help understand it
# http://www.umiacs.umd.edu/research/EXPAR/papers/3449/node8.html

# the filter smoothens out the curve without discarding the extreme 
# datapoints, it factors them in but normalizes their value using
# neighbouring datapoints 

def plot(rssi_series, window, average_series, limit=10):
        # COMMENT OUT IF YOU WANT TO PLOT THE ROLLING AVERAGE AND THE RSSI SERIES
    df_rssi_series= pd.DataFrame(rssi_series, columns=['rssi'])
    df_rssi_series['pd rolling ave'] = df_rssi_series['rssi'].rolling(window=window, min_periods=1).mean()
    df_rssi_series['calculated rolling ave'] = average_series[:100500]
    df_rssi_series.plot(title='window size: '+str(window))
    plt.show()


def nearest_neighbor( rssi_series, params, df_rssi_series=None):
    """
    Runs nearest neighbor kernel smoother over the values.
    See https://en.wikipedia.org/wiki/Kernel_smoother
    :param params: dict with following values

    :param rssi_series: rssi measurents
    :param window: the size of the window that the filter will use to smooth out the curve
                    larger window size - more smooth curve, 
                        extreme points have smaller impact on the filtered data
                    smaller window size - extreme points have greater impact on the filtered data

    :param verbose: not sure what it does, isn't used here at all
    :return: returns flitered out data centered at around 0
    """
    # Extract params
    window = int(params["window"])  # expect an int
    verbose = bool( params["verbose"] ) # expect a bool
    average_series = list()

    # initializes the entry values for the filtering process
    average_series = list()
    current_index = 0
    values_in_window = 0
    window_sum = 0
    n = len(rssi_series)

    # Initialize window, hereafter continue until window is empty
    value = rssi_series[current_index]
    current_index += 1 # index number of rssi measurement
    values_in_window += 1 # number of values in the window
    window_sum += value # sum in the window

    # Handle start case until window is full
    # it is impoportant to note that the filter will iterate through datapoints
    # untill the left edge of the window doesnt have ane values e.g.:
    #  rssi = [a,b, c, d, e, f, g, h, i, j, k, l, m]
    #  window =                            [k, l, m, x, x, x]  
    # window size=6, rolling ave = (k+l+m)/3, it results in n + window filtered datapoints
    # other rolling averages tend to end when the right edge of the window doesn't see any new values
    while( values_in_window > 0 ):
        filtered_value = window_sum / values_in_window
        average_series.append(filtered_value)

        # Remove if window is too big
        '''once the window gets populated the code starts to discard the oldest values 
        to make room for the new ones'''
        if( current_index >= window ):
            value = rssi_series[current_index-window]
            values_in_window -= 1
            window_sum -= value

        # Add value if we can
        if( current_index < n ):
            value = rssi_series[current_index]
            values_in_window += 1
            window_sum += value

        # Always move forward
        current_index += 1


    #plot(rssi_series, window, average_series)




    # Now remove the estimated averager from values
    filtered_series = list()
    '''the filtering process subtrackts from  the original rssi 
        the rolling average value of the [x + floor(window_size/2)] index
        so the subtraction has an offset of half of the window size
        
        this process normalizes (I think that's what it is called) the values (centeres them around 0)

        '''
    for i in range( n ):
        value = rssi_series[i]
        average_value = average_series[i+ (window//2)]
        filtered_series.append( value - average_value )
    


    return filtered_series




def lowpass_lagged( rssi_series, params):
    # See https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average

    #
    # Noticed that EWMA lags behind signal trend changes (slow to react).
    # This results in long sequences of 0's or 1's, performs poorly on run tests.
    # Can perhaps adjust alpha but lagged weighted average perhaps more appropriate.
    #
    # Extract params
    alpha = float(params["alpha"])     # expect an float
    lag   = int(params["lag"])         # expect an int
    #verbose = bool(params["verbose"])  # expect a bool

    lagged_series = list()
    for i in range(lag, len(rssi_series) ):
        current_value = rssi_series[i]
        lagged_value = rssi_series[i-lag]
        filtered_value = current_value + (current_value - lagged_value)
        lagged_series.append( filtered_value )

    filtered_series = lowpass( lagged_series, alpha )
    return filtered_series

# BAD NAME, ACTUALLY HIGH PASS ACHIEVED BY SUBTRACTiNG LOW FREQUENCY
def lowpass( rssi_series, alpha):
    """
    Makes a key from the rssi values with discrete low-pass filter (EWMA) to threshold the signal.
    Equivalent to subtracting the low frequencies from the signal to leave the high frequencies.
    May return list of length less than rssiSeries.
    param rssi_series list of float rssi values
    param alpha float between 0.0 and 1.0 for EWMA
    param epsilon float (typically less than 1.0) to determine confidence of key bits
          larger means fewer keybits but more confidence in those keybits
          smaller means more keybits but less certainty in them
    return tuple of two lists, list of int values in {-1,0,1} and list of EWMA values
    """


    moving_average_series = ewma( rssi_series, alpha )
    #moving_average_series = nearest_neighbor(rssi_series, params)

    # We use an epsilon to filter when rssi is not changing, we end up picking
    # long strings because it will never be exactly equal because we are dealing with doubles
    # epsilon = 0.1 # in units of rssi
    # Quantize using the ewma rssi and raw rssi
    filtered_series = list()
    for i in range(len(rssi_series)):
        value = rssi_series[i]
        moving_average_value = moving_average_series[i]
        diff_value = value - moving_average_value
        filtered_series.append( diff_value )

    return filtered_series


def highpass( rssi_series, alpha ):
    """
    Makes a key from the rssi values by removing low frequencies with discrete high-pass filter.
    May return list of length less than rssiSeries.
    param rssi_series list of float rssi values
    param alpha float between 0.0 and 1.0 for filter
    param epsilon float (typically less than 1.0) to determine confidence of key bits
          larger means fewer keybits but more confidence in those keybits
          smaller means more keybits but less certainty in them
    return tuple of two lists, list of int values in {-1,0,1} and list of EWMA values
    """
    # Extract params

    # We use an epsilon to filter when rssi is not changing, we end up picking
    # long strings because it will never be exactly equal because we are dealing with doubles
    #epsilon = 0.1 # in units of rssi

    # Quantize using the ewma rssi and raw rssi
    filtered_series = list()

    #
    # Noticed that EWMA lags behind signal trend changes (slow to react).
    # This results in long sequences of 0's or 1's.
    # Can perhaps adjust alpha but this does poorly at identifying the low frequencies.
    # We would like to keep alpha but better align the original and delayed EWMA.
    # This is what the timeOffset does.
    #
    # Found setting to 1 for example significantly improved run test (2.03, 2.04) performance.
    # It does degrade other performance though relatively minor.
    #
    filtered_series.append( 0.0 ) # seed filtered series to expected value
    for i in range( 1, len(rssi_series) ):
        xi   = rssi_series[i]
        xi_1 = rssi_series[i-1]
        yi_1 = filtered_series[i-1]
        filtered_value = alpha * ( yi_1 + xi - xi_1 )
        filtered_series.append(filtered_value)
    return filtered_series


def ewma( rssi_series, alpha ):
    """
    Computes a new series with exponentially weighted moving average.
    The alpha is current value weight while (1-alpha) is history weight.
    Effectively a low pass filter (see https://en.wikipedia.org/wiki/Low-pass_filter)
    returns a list of same length as series
    """
    beta = 1.0 - alpha
    filtered_series = list()
    i = 0
    filtered_series.append(rssi_series[i])  # seed with initial value
    i = i + 1
    while (i < len(rssi_series)):
        history = filtered_series[i - 1]
        current = rssi_series[i]
        filtered_series.append((alpha * current) + (beta * history))
        i = i + 1
    return filtered_series

def bandpassHPLP(rssi_values, alphaLP, alphaHP, verbose=False):
    """
    First performs high pass filter followed by low pass filter.
    Not very effective band pass filter but computationally easy.
    :param rssi_values:
    :param alphaLP:
    :param alphaHP:
    :param verbose:
    :return:
    """
    # ewmaAlice = ewma( rssiAlice, alpha )
    # Run low-pass filter first (want to lose actual noise, not agreed between Alice and Bob)
    filtered_series = highpass(rssi_values, alphaHP)

    # Run high-pass filter (get rid of any trends to bounce around zero)
    # overwrite the low-pass results
    return lowpass(filtered_series, alphaLP)

def bandpassLPHP( rssi_values, alphaLP, alphaHP, verbose=False ):
    """
    First performs low pass filter followed by high pass filter.
    Not very effective band pass filter but computationally easy.
    :param rssi_values:
    :param alphaLP:
    :param alphaHP:
    :param verbose:
    :return:
    """
    # ewmaAlice = ewma( rssiAlice, alpha )
    # Run low-pass filter first (want to lose actual noise, not agreed between Alice and Bob)
    filtered_series = lowpass(rssi_values, alphaLP)

    # Run high-pass filter (get rid of any trends to bounce around zero)
    # overwrite the low-pass results
    return highpass(filtered_series, alphaHP, verbose)

def difference_backwards( rssi_series, params ):
    """
    Detrends by taking difference between successive values.  Centers around zero.
    See https://en.wikipedia.org/wiki/Finite_difference, approximates derivative.
    https://www.youtube.com/watch?v=kkiVU--r9pI
    I believe this is a backwards difference.
    Returns list that is one shorter than len(rssi_series).  Thus if a 128 length
    is desired, a 129 length series needs to be input.
    """
    # Extract params
    h = int(params["h"])  # expect an int
    
    filtered_series = list()
    i = h
    while (i < len(rssi_series)):
        history = rssi_series[i-h]
        current = rssi_series[i]
        filtered_series.append( current - history )
        i = i + 1
    return filtered_series