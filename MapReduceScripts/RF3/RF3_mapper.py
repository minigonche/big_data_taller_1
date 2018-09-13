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
        date_string = values[1]
        date = datetime.strptime(date_string,date_format)
        return(date)

    # End Date
    elif(key.upper() == 'END_DATE'):
        if(length_of_line == 3): # Header does not have an end date
            return(None)
        else:
            date_string = values[2]
            date = datetime.strptime(date_string,date_format)
            return(date)

    # Start Location
    elif(key.upper() == 'START_LOC'):

        #Only certain lengths have start location:
        if(length_of_line in [3,5,17,19]):
            if(length_of_line == 3):
                return(values[2])

            if(length_of_line == 5):
                return(values[3])

            if(length_of_line == 17):
                return(values[7])

            if(length_of_line == 19): # More than one type of header has this length                
                #Checks that is not a coordinate (lattitude or longitud)
                if('.' in values[5] or values[5] == 0):
                    return(None)
                else:
                    return(values[5])

        else:
            return(None)


    # End Location
    elif(key.upper() == 'END_LOC'):

        #Only certain lengths have end location:
        if(length_of_line in [5,17,19]):
            
            if(length_of_line == 5):
                return(values[4])

            if(length_of_line == 17):
                return(values[8])

            if(length_of_line == 19): # More than one type of header has this length                
                #Checks that is not a coordinate (lattitude or longitud)
                if('.' in values[6] or values[6] == 0):
                    return(None)
                else:
                    return(values[6])

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


# 1 Newwark
# 132 JFK
# 138 La Guardia
airports = ['1','132','138']
#airports = ['1','132','138', '181', '229', '171', '7', '89', '24']

lens = {}

# input comes from STDIN (standard input)
# Input enters in a CSV scheme
# Each line is a record
for line in sys.stdin:

    line = line.strip()
    values = line.split(',')

    from_location =  get_value('START_LOC', values)# From Location
    to_location = get_value('END_LOC', values) # To Location

    start_date = get_value('START_DATE', values) #Start Date

    
    #Process and prints

    # Only prints if all values are not None
    if(from_location is not None and
       to_location is not None and
       start_date is not None):
        

        #Only prints if from location is airport
        if(from_location in airports):

            day_of_week = start_date.isoweekday()
            minute_of_day = start_date.hour*60 + start_date.minute
            airport_code = from_location
            destination = to_location
            number_of_trips = 1

            #day_of_week tab minute_of_day tab airport_code tab destination:number_of_trips
            print('%s\t%s\t%s\t%s:%s' % (day_of_week, minute_of_day,airport_code,destination,number_of_trips))



