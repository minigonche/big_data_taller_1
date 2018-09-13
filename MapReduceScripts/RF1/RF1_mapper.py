#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana
'''

import sys
from datetime import datetime

def mapper(start, end):

    # input comes from STDIN (standard input)
    # Input enters in a CSV scheme
    # Each line is a record
    for line in sys.stdin:
        data = line.split(',')

        # reading from a Yellow-type file (17)
        if len(data) == 17:
            destination = data[6]
            pickupTime = data[1]

        # reading from a Green-type file (18)
        if len(data) == 18:
            destination = data[6]
            pickupTime = data[1]

        # reading from a FHV-type file (17)
        if len(data) == 5:
            destination = data[4]
            pickupTime = data[1]

        pickupTime = datetimeToInt(pickupTime)

        if inTimeRange(start, end, pickupTime):
            print('%s\t%s\t%s' % (destination, 1))

# converts time to integer
def datetimeToInt(datetimeString):

        #change if you wish to hide error printout
        print_errors = True

        #Date Format YYYY-MM-DD hh:mm:ss
        format = '%Y-%m-%d H:%M:%S'
        hour = None

        try:
            date = datetime.strptime(datetimeString,format)
            #hour is in range(24)
            hour = int(date.time.hour)
            return hour

        except ValueError:
            if(print_errors):
                print('Incorrect format: '  + datetimeString)

# takes a starting hour and an end hour to find out if an specific time is in range
def inTimeRange(start, end, time):
    if time and (int(start) <= int(time)) and (int(time) <= int(end)):
        return True
    else: return False

mapper(11,12)
