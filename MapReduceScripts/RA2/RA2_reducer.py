#!/usr/bin/env python
"""RF2_reducer.py"""

from operator import itemgetter
import sys
#Reducer para el Requerimiento Analitico 2 del Taller 1


# input comes from STDIN
# Input follows the format:
# moment tab hour_of_day tab source_1:destination_1:number_of_trips_1;source_2:destination_2:number_of_trips_1
# Output format
# Same

saved = {}

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    moment, hour_of_day, trips = line.split('\t')

    #Saves the new input

    if(moment not in saved):
        saved[moment] = {}

    if(hour_of_day not in saved[moment]):
        saved[moment][hour_of_day] = {}


    current_dic = saved[moment][hour_of_day]

    for trip in trips.split(';'):

        if(trip):
            source, dest, num_trips = trip.split(':')
            #Updates Structures
            if(source in current_dic):
                if(dest in current_dic[source]):
                    current_dic[source][dest] = current_dic[source][dest] +  int(num_trips)
                else:
                    current_dic[source][dest] = int(num_trips)
            else:
                current_dic[source] = {}
                current_dic[source][dest] = int(num_trips)




#Exports Saved Dictionary

for moment in saved.keys():
    for hour_of_day in saved[moment].keys():
        print_string = ''

        for source in saved[moment][hour_of_day].keys():
            for dest in saved[moment][hour_of_day][source].keys():
                print_string = print_string + source + ":" + dest + ':' + str(saved[moment][hour_of_day][source][dest]) + ';'

        print('%s\t%s\t%s' % (moment, hour_of_day,print_string))
