#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana.
'''
import os
import sys
from datetime import datetime

#init

start = 10
end = 11

location_dictionary = {'Borough': ['LocationID'], 'EWR': ['1'], 'Queens': ['2', '7', '8', '9', '10', '15', '16', '19', '27', '28', '30', '38', '53', '56', '57', '64', '70', '73', '82', '83', '86', '92', '93', '95', '96', '98', '101', '102', '117', '121', '122', '124', '129', '130', '131', '132', '134', '135', '138', '139', '145', '146', '157', '160', '171', '173', '175', '179', '180', '191', '192', '193', '196', '197', '198', '201', '203', '205', '207', '215', '216', '218', '219', '223', '226', '252', '253', '258', '260'], 'Bronx': ['3', '18', '20', '31', '32', '46', '47', '51', '58', '59', '60', '69', '78', '81', '94', '119', '126', '136', '147', '159', '167', '168', '169', '174', '182', '183', '184', '185', '199', '200', '208', '212', '213', '220', '235', '240', '241', '242', '247', '248', '250', '254', '259'], 'Manhattan': ['4', '12', '13', '24', '41', '42', '43', '45', '48', '50', '68', '74', '75', '79', '87', '88', '90', '100', '103', '104', '105', '107', '113', '114', '116', '120', '125', '127', '128', '137', '140', '141', '142', '143', '144', '148', '151', '152', '153', '158', '161', '162', '163', '164', '166', '170', '186', '194', '202', '209', '211', '224', '229', '230', '231', '232', '233', '234', '236', '237', '238', '239', '243', '244', '246', '249', '261', '262', '263'], 'Staten Island': ['5', '6', '23', '44', '84', '99', '109', '110', '115', '118', '156', '172', '176', '187', '204', '206', '214', '221', '245', '251'], 'Brooklyn': ['11', '14', '17', '21', '22', '25', '26', '29', '33', '34', '35', '36', '37', '39', '40', '49', '52', '54', '55', '61', '62', '63', '65', '66', '67', '71', '72', '76', '77', '80', '85', '89', '91', '97', '106', '108', '111', '112', '123', '133', '149', '150', '154', '155', '165', '177', '178', '181', '188', '189', '190', '195', '210', '217', '222', '225', '227', '228', '255', '256', '257'], 'Unknown': ['264', '265']}


def location_by_ID_lookup(location_dictionary, value):
    '''
    This method uses the dictionary created by the location_by_ID method
    to return the Borough (e.g. Queens, Bronx...) of an specific value.
    '''
    keys = list(location_dictionary.keys())

    for key in keys:
        if str(value) in location_dictionary[key]:
            return(key)


#Extractor Method
def get_value(key, values):
    """ Gets the value of a given key
    This method was created to overcome the fact that files have different
    headers and not all values can be found in all files. This method was constructed based on
    the file: 'headers_sorted.txt', where all possible headers are sorted by length and have their
    occurence rate.
    #Note: The method also checks for empty values and if is a header. In both cases returns
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

    if start << end:
        if time and (int(start) <= int(time)) and (int(time) <= int(end)):
            return True
        else: return False



# input comes from STDIN (standard input)
# Input enters in a CSV scheme
# Each line is a record
for line in sys.stdin:
    line = line.strip()
    data = line.split(',')

    destinationID = get_value('END_LOC', data)
    destination = location_by_ID_lookup(location_dictionary, destinationID)

    pickupTime = get_value('START_DATE', data)
    pickupTime = datetimeToInt(pickupTime)
    if destination:
        if inTimeRange(start, end, pickupTime):
            print('%s\t%s' % (destination, 1))



