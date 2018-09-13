#!/usr/bin/env python
"""RF2_reducer.py"""

from operator import itemgetter
import sys
#Reducer para el RF2 del Taller 1


# input comes from STDIN
# Input follows the format: 
# number_of_month tab sum_of_total_costs tab number_of_trips
# Output format
# Same

totals = {}

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    key, count = line.split('\t')

    #Updates Structures
    if(key in totals):
        totals[key] = totals[key] + int(count)        
    else:
        totals[key] = int(count)
        


for key in totals.keys():
    print('%s\t%s' % (key, totals[key]))

