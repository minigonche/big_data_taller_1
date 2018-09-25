#!/usr/bin/env python
"""RF2_reducer.py"""

from operator import itemgetter
import sys
#Reducer para el Requerimiento Funcional 3 del Taller 1


# input comes from STDIN
# Input follows the format: 
#day_of_week tab minute_of_day tab airport_code tab destination_1:number_of_trips_1;destination_2:number_of_trips_1
# Output format
# Same

saved = {}

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    day_of_week, minute_of_day, airport_code, destinations = line.split('\t')

    #Saves the new input

    if(day_of_week not in saved):
        saved[day_of_week] = {}

    if(minute_of_day not in saved[day_of_week]):
        saved[day_of_week][minute_of_day] = {}

    if(airport_code not in saved[day_of_week][minute_of_day]):
        saved[day_of_week][minute_of_day][airport_code] = {}


    current_dic = saved[day_of_week][minute_of_day][airport_code]

    for dest_str in destinations.split(';'):

        if(dest_str):
            dest_code, num_trips = dest_str.split(':')
            #Updates Structures
            if(dest_code in current_dic):
                current_dic[dest_code] = current_dic[dest_code] + int(num_trips)            
            else:
                current_dic[dest_code] = int(num_trips)     


#Exports Saved Dictionary

for day_of_week in saved.keys():
    for minute_of_day in saved[day_of_week].keys():
        for airport_code in saved[day_of_week][minute_of_day].keys():

            print_string = ''

            for dest in saved[day_of_week][minute_of_day][airport_code].keys():
                print_string = print_string + dest + ':' + str(saved[day_of_week][minute_of_day][airport_code][dest]) + ';'

            print('%s\t%s\t%s\t%s' % (day_of_week, minute_of_day,airport_code,print_string))


