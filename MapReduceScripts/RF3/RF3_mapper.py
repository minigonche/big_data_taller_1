#!/usr/bin/env python
# coding=utf-8
"""RF2_mapper.py"""
import sys
import re
from datetime import datetime
# Mapper para el Requerimiento Funcional 3 del Taller 1

# Displays the location and amount of trips per minute out of every airport

# Asumptions
# Will only record start date of trips

# The output format is:
# day_of_week tab minute_of_day tab airport_code tab destination:number_of_trips

# If displays errors and warnings
print_errors = True


# 1 Newwark
# 132 JFK
# 138 La Guardia
airports = [1,132,138]

lens = {}

# input comes from STDIN (standard input)
# Input enters in a CSV scheme
# Each line is a record
for line in sys.stdin:
    values = line.split(',')

    from_location = None # From Location
    to_location = None # To Location

    start_date = None #Start Date


    if (len(values)) in lens:
        lens[len(values)] = lens[len(values)] + 1
    else:
        lens[len(values)] = 1
    
    # Is Yellow Taxi (18 Values)
    if(len(values) == 18):
        #Date Format 2017-01-09 11:13:28
        format = '%Y-%m-%d %H:%M:%S'

        # Gets the start date
        date_string = values[1]
        try:
            start_date = datetime.strptime(date_string,format)
        except ValueError:
            if(print_errors):
                print('Start Date not in Format: '  + date_string)
        
        # Gets the from location ID
        from_location_str = values[5]
        try:
            from_location = int(from_location_str)
        except ValueError:
            if(print_errors):
                print('From location not numeric: '  + from_location_str)

        # Gets the to location ID
        to_location_str = values[5]
        try:
            to_location = int(to_location_str)
        except ValueError:
            if(print_errors):
                print('To location not numeric: '  + to_location_str)


    # Is Green Taxi (21 Values)
    elif(len(values) in [19,21]):

        #Date Format 2017-01-09 11:13:28
        format = '%Y-%m-%d %H:%M:%S'

        # Gets the start date
        date_string = values[1]
        try:
            start_date = datetime.strptime(date_string,format)
        except ValueError:
            if(print_errors):
                print('Start Date not in Format: '  + date_string)
        
        # Gets the from location ID
        from_location_str = values[5]
        try:
            from_location = int(from_location_str)
        except ValueError:
            if(print_errors):
                print('From location not numeric: '  + from_location_str)

        # Gets the to location ID
        to_location_str = values[5]
        try:
            to_location = int(to_location_str)
        except ValueError:
            if(print_errors):
                print('To location not numeric: '  + to_location_str)

        

    # Is Empty line
    else:
        if(print_errors):
            print('Empty Line')
        continue

    
    #Process and prints

    # Sunday is 7
    # Only prints if all values are not None
    if(from_location is not None and
       to_location is not None and
       start_date is not None):

        #Only prints if from location is airport
        if(from_location in airports):

            day_of_week = date.isoweekday()
            minute_of_day = date.hour*60 + date.minute
            airport_code = from_location
            destination = to_location
            number_of_trips = 1

            #day_of_week tab minute_of_day tab airport_code tab destination:number_of_trips
            print('%s\t%s\t%s\t%s:%s' % (day_of_week, minute_of_day,airport_code,destination,number_of_trips))



print(lens)