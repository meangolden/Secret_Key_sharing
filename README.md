# Secret_Key_sharing
Created the frist file. This file carries the functions that will be used later on in the main file
'''

    EXAMPLE TO RUN:
        python3 testFilters.py ../data3_upto5.mat 2 2 6 300 1 1



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
