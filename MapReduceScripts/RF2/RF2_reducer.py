#!/usr/bin/env python
"""RF2_reducer.py"""

from operator import itemgetter
import sys, traceback
#Reducer para el RF2 del Taller 1


# input comes from STDIN
# Input follows the format: 
# number_of_month tab sum_of_total_costs tab number_of_trips
# Output format
# Same


totals = {}
counts = {}

for line in sys.stdin:
    try:
        # remove leading and trailing whitespace
        line = line.strip()

        # parse the input we got from mapper.py
        month, total, count = line.split('\t')

        #Updates Structures
        if(month in totals):
            totals[month] = totals[month] + float(total)
            counts[month] = counts[month] + float(count)
        else:
            totals[month] = float(total)
            counts[month] = float(count)

    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60


for month in totals.keys():
    try:
        print('%s\t%s\t%s' % (month, totals[month], counts[month]))
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60




