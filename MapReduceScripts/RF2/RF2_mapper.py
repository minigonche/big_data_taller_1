#!/usr/bin/env python
# coding=utf-8
"""RF2_mapper.py"""
import sys
import re
from datetime import datetime
# Mapper para el Requerimiento Funcional 2 del Taller 1

# Displays the average cost amount of all trips that took place on a sunday
# on a given month

# The output format is:
# number_of_month tab sum_of_total_costs tab number_of_trips

# Assumptions
# If trip starts on a saturday and ends on a sunday, will be recorded

# If displays errors and warnings
print_errors = False

# input comes from STDIN (standard input)
# Input enters in a CSV scheme
# Each line is a record
for line in sys.stdin:
    values = line.split(',')
    start_month = None # Start Month of the year
    start_week_day = None # Start Weekday of the year

    end_month = None # End Month of the year
    end_week_day = None # End Weekday of the year

    total_cost = None # Total cost of the trip

    
    # Is Yellow Taxi (18 Values)
    if(len(values) == 18):
        #Date Format 2017-01-09 11:13:28
        format = '%Y-%m-%d %H:%M:%S'

        # Gets the start date
        date_string = values[1]
        try:
            date = datetime.strptime(date_string,format)
            start_month = date.month
            start_week_day = date.isoweekday()
        except ValueError:
            if(print_errors):
                print('Start Date not in Format: '  + date_string)

        # Gets the end date
        date_string = values[2]
        try:
            date = datetime.strptime(date_string,format)
            end_month = date.month
            end_week_day = date.isoweekday()
        except ValueError:
            if(print_errors):
                print('End Date not in Format: '  + date_string)

        # Gets the total Value
        cost_string = values[-1]
        try:
            total_cost = float(cost_string)
        except ValueError:
            if(print_errors):
                print('Total cost is not numeric: '  + cost_string)

    # Is Green Taxi (21 Values)
    elif(len(values) == 21):

        #Date Format 2017-01-09 11:13:28
        format = '%Y-%m-%d %H:%M:%S'

        # Gets the start date
        date_string = values[1]
        try:
            date = datetime.strptime(date_string,format)
            start_month = date.month
            start_week_day = date.isoweekday()
        except ValueError:
            if(print_errors):
                print('Start Date not in Format: '  + date_string)

        # Gets the end date
        date_string = values[2]
        try:
            date = datetime.strptime(date_string,format)
            end_month = date.month
            end_week_day = date.isoweekday()
        except ValueError:
            if(print_errors):
                print('End Date not in Format: '  + date_string)

        # Gets the total Value
        cost_string = values[-3]
        try:
            total_cost = float(cost_string)
        except ValueError:
            if(print_errors):
                print('Total cost is not numeric: '  + cost_string)
        

    # Is Empty line
    else:
        if(print_errors):
            print('Empty Line')
        continue

    
    #Process and prints

    # Sunday is 7
    # Only prints if all values are not None
    if(start_month is not None and
       start_week_day is not None and
       end_month is not None and
       end_week_day is not None and
       total_cost is not None):



        # Start Date
        if(start_week_day == 7):
            print('%s\t%s\t%s' % (start_month, total_cost,1))
        # End Date
        elif(end_week_day == 7):
            print('%s\t%s\t%s' % (end_month, total_cost,1))


