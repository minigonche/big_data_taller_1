#!/usr/bin/env python
"""RF2_reducer.py"""

from operator import itemgetter
import sys
#Reducer para el Requerimiento Analitico 2 del Taller 1


# input comes from STDIN
# Input follows the format: 
#day_of_week tab hour_of_day tab source_1:destination_1:number_of_trips_1;source_2:destination_2:number_of_trips_1
# Output format
# Same

saved = {}

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    day_of_week, hour_of_day, trips = line.split('\t')

    #Saves the new input

    if(day_of_week not in saved):
        saved[day_of_week] = {}

    if(hour_of_day not in saved[day_of_week]):
        saved[day_of_week][hour_of_day] = {}


    current_dic = saved[day_of_week][hour_of_day]

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

for day_of_week in saved.keys():
    for hour_of_day in saved[day_of_week].keys():
        print_string = ''

        for source in saved[day_of_week][hour_of_day].keys():
            for dest in saved[day_of_week][hour_of_day][source].keys():
                print_string = print_string + source + ":" + dest + ':' + str(saved[day_of_week][hour_of_day][source][dest]) + ';'

        print('%s\t%s\t%s' % (day_of_week, hour_of_day,print_string))


