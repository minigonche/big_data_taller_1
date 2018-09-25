#!/usr/bin/env python
# coding=utf-8
"""RA2_mapper.py"""
import sys
import re
from datetime import datetime
from sets import Set
# Mapper para el Requerimiento Analitico 2 del Taller 1

# Displays the trips between zones, per hour of day of week

# Asumptions
# Only checks for start time of trip

# The output format is:
# day_of_week (in text) tab hour_of_day tab source:destinarion:num_of_trips
# day_of_month tab hour_of_day tab source:destinarion:num_of_trips

# If displays errors and warnings
print_errors = True

weekdays = ['MON','TUE','WED','THU','FRI','SAT','SUN']

#current supported zones
zones = Set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', 
        '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', 
        '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', 
        '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', 
        '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', 
        '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', 
        '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', 
        '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', 
        '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', 
        '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263'])


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


        day_of_week = start_date.weekday()
        day_of_month = start_date.day

        hour_of_day = start_date.hour
        source = from_location
        destination = to_location
        number_of_trips = 1
        
        if(source in zones and destination in zones):       
            
            #day_of_week (in text) tab minute_of_day tab airport_code tab destination:number_of_trips
            print('%s\t%s\t%s:%s:%s' % (weekdays[day_of_week], hour_of_day, source, destination,number_of_trips))

            #day_of_month tab minute_of_day tab airport_code tab destination:number_of_trips
            print('%s\t%s\t%s:%s:%s' % (day_of_month, hour_of_day, source, destination,number_of_trips))
