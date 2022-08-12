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
    # untill the left edge of the window doesnt have ane values i.e.:
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
