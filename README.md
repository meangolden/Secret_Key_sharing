## Project Title

Filtering Algorithms Comparison

## Description

This program compares results for different sets of parameters across different filtering algorithms:

- NEAREST NEIGHBOURS
- lowpass lagged
- EWMA (exponentially weighted moving average, probably doesn't work)
- bandpassHPLP
- bandpassLPHP

The program extracts only 20,000 datapoints to speed up the process. The values that are printed are the number of mismatches between Alice and Bob keys, the value is printed out just to see the speed of the program.

## Inputs

The following inputs are required:

- `filename`: the name of the file that contains the data
- `var_factor`: the multiplier of variance to set the limit to quantize
- `N`: number of bits to quantize to
- `block_size`: length of the key stretch
- `length_of_key`: length of the key
- `threshold`: 

## Outputs

The program outputs `filters.csv` and `filters.html`, whichever is more convenient.

## Execution

To run the program, execute the following command:

python3 testFilters.py ../data3_upto5.mat 2 2 6 300 1 1


## Notes

Since there are about 500 iterations, no graphs are made. On my machine, the program runs for 12 minutes. I am working on splitting the computations to different processor cores.
