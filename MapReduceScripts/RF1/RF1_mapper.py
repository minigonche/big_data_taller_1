#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana.

TEST
'''
import os
import sys
from datetime import datetime
import numpy as np

def location_by_ID(value):
    #Absolute path, script is in
    script_dir = os.path.dirname(__file__)
    #relative path
    rel_path = 'LocationByID/taxi_zone_lookup.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    # get data to format index to use in location by data method
    f = open(abs_file_path, 'r')
    data = f.read()
    data = data.split('\n')

    zones = []
    location_by_ID = {}
    locations = []

    for line in data:
        line = line.strip()
        #print(line)
        location, zone, trash = line.split(',', 2)

        if zone not in zones:
            location_by_ID[zone] = []

    for line in data:
        line = line.strip()
        location, zone, trash = line.split(',', 2)

        if (location not in location_by_ID[zone]):
            location_by_ID[zone].append(location)

    keys = list(location_by_ID.keys())

    for key in keys:
        if str(value) in location_by_ID[key]:
            return(key)


#Extractor Method
def get_value(key, values):
    """ Gets the value of a given key
    This method was created to overcome the fact that files have different
    headers and not all values can be found in all files. This method was constructed based on
    the file: 'headers_sorted.txt', where all possible headers are sorted by length and have their
    occurence rate.
    #Note: The method also checks for empy values and if is a header. In both cases returns
        None for any given key
    # Important: Don't forget to strip line before splitting!

    Parameters:
        key : String
            Should be one of the following:
                - START_DATE: start date of the trip. Returns Date or None
                - END_DATE: start date of the trip. Returns Date or None
                - START_LOC: Start loaction of trip (The ID of the location). Returns String or None
                - END_LOC: End loaction of trip (The ID of the location). Returns String or None
                - COST: The cost of the trip: Returns Float or None
        values : list
            Corresponds to the splitted input line (splitted by comma)

    Returns:
        The corresponding value of the key (already in its type:)
    """


    date_format = '%Y-%m-%d %H:%M:%S'
    length_of_line = len(values)

    if(length_of_line == 0 or not(values[0]) or 'vendor' in values[0].lower() or 'dispatching' in values[0].lower()): #line is empty or header
        return(None)

    # Start Date
    elif(key.upper() == 'START_DATE'):

        try:
            date_string = values[1]

            if(date_string == ''):
                return(None)

            date = datetime.strptime(date_string,date_format)
            return(date)
        except ValueError:
             if(print_errors):
                print('Date not in format: : ' + date_string)
                return(None)

    # End Date
    elif(key.upper() == 'END_DATE'):
        try:
            if(length_of_line == 3): # Header does not have an end date
                return(None)
            else:
                date_string = values[2]

                if(date_string == ''):
                    return(None)

                date = datetime.strptime(date_string,date_format)
                return(date)
        except ValueError:
             if(print_errors):
                print('Date not in format: : ' + date_string)
                return(None)

    # Start Location
    elif(key.upper() == 'START_LOC'):

        #Only certain lengths have start location:
        if(length_of_line in [3,5,17,19]):

            start_loc = None
            if(length_of_line == 3):
                start_loc = values[2]

            if(length_of_line == 5):
                start_loc = values[3]

            if(length_of_line == 17):
                start_loc = values[7]

            if(length_of_line == 19): # More than one type of header has this length
                #Checks that is not a coordinate (lattitude or longitud)
                if('.' in values[5] or values[5] == 0):
                    return(None)
                else:
                    start_loc = values[5]

            if(start_loc == ''):
                return(None)

            return(start_loc)

        else:
            return(None)


    # End Location
    elif(key.upper() == 'END_LOC'):

        #Only certain lengths have end location:
        if(length_of_line in [5,17,19]):

            end_loc = None
            if(length_of_line == 5):
                end_loc = values[4]

            elif(length_of_line == 17):
                end_loc = values[8]

            elif(length_of_line == 19): # More than one type of header has this length
                #Checks that is not a coordinate (lattitude or longitud)
                if('.' in values[6] or values[6] == 0):
                    return(None)
                else:
                    end_loc = values[6]

            if(end_loc == ''):
                return(None)

            return(end_loc)

        else:
            return(None)


    #Cost
    elif(key.upper() == 'COST'):

        #Only certain lengths have end location:
        if(length_of_line in [17,18, 19, 20, 21]):

            if(length_of_line in [17,18]):

                try:
                    return(float(values[-1]))

                except ValueError:
                    if(print_errors):
                        print('Cost not in float format: ' + values[-1])
                    return(None)


            if(length_of_line in [20,21]):

                try:
                    return(float(values[-3]))

                except ValueError:
                    if(print_errors):
                        print('Cost not in float format: ' + values[-3])
                    return(None)


            if(length_of_line == 19): # Different headers have ths length

                #Difference can be determined from value at position 3, from the columns: store_and_fwd_flag
                if(values[3] in ['Y','N']):
                    ind = -3
                else:
                    ind = -1

                try:
                    return(float(values[ind]))

                except ValueError:
                    if(print_errors):
                        print('Cost not in float format: ' + values[ind])
                    return(None)

        else:
            return(None)

    else:
        if(print_errors):
            print('Key: ' + values[ind])
        return(None)


def mapper(start, end):

    # input comes from STDIN (standard input)
    # Input enters in a CSV scheme
    # Each line is a record
    for line in sys.stdin:
        line = line.strip()
        data = line.split(',')

        destinationID = get_value('END_LOC', data)
        destination = location_by_ID(destinationID)

        pickupTime = get_value('START_DATE', data)
        pickupTime = datetimeToInt(pickupTime)
        if destination:
            if inTimeRange(start, end, pickupTime):
                print('%s\t%s' % (destination, 1))

# converts time to integer
def datetimeToInt(datetimeString):

#Date Format YYYY-MM-DD hh:mm:ss
    format = '%Y-%m-%d H:%M:%S'
    hour = None
    if datetimeString:
        try:
            #hour is in range(24)
            hour = int(datetimeString.hour)
            return hour

        except ValueError:
            if(print_errors):
                print('Incorrect format: '  + datetimeString)

# takes a starting hour and an end hour to find out if an specific time is in range
def inTimeRange(start, end, time):
    if time and (int(start) <= int(time)) and (int(time) <= int(end)):
        return True
    else: return False
    

#Run mapper method within a time range mapper(a, b)
mapper(10, 11)    
