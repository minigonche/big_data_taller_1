#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import datetime


format = '%Y-%m-%d %H:%M:%S'

def isThanksGiving(pickup_time):
    #its in november
    thanksGivingDayDict = {2009: 26, 2010: 25, 2011: 24, 2012: 22, 2013: 28, 2014: 27, 2015: 26,
                    2016: 24, 2017: 23, 2018: 22}
    memorialDay = thanksGivingDayDict[pickup_time.year]

    if (pickup_time.month == 11) and (pickup_time.day == memorialDay):
        return True
    else:
        return False

def isMemorialDay(pickup_time):
    #its in may
    memorialDayDict = {2009: 25, 2010: 31, 2011: 30, 2012: 28, 2013: 27, 2014: 26, 2015: 25,
                    2016: 30, 2017: 29, 2018: 28}
    memorialDay = memorialDayDict[pickup_time.year]

    if (pickup_time.month == 5) and (pickup_time.day == memorialDay):
        return True
    else:
        return False

def isLaborDay(pickup_time):

    laborDayDict = {2009: 7, 2010: 6, 2011: 5, 2012: 3, 2013: 2, 2014: 1, 2015: 7, 2016: 5, 2017: 4, 2018: 3}
    laborDay = laborDayDict[pickup_time.year][0]

    if (pickup_time.month == 9) and (pickup_time.day == laborDay):
        return True
    else:
        return False

def isChristmas(pickup_time):

    if (pickup_time.month == 12) and (pickup_time.day == 25 or pickup_time.day == 24):
        return True
    else:
        return False

def isNewYears(pickup_time):

    if (pickup_time.month == 12 and pickup_time.day == 31):
        return True
    else:
        return False

def isValentines(pickup_time):

    if (pickup_time.month == 2) and (pickup_time.day == 14):
        return True
    else:
        return False

def isSummer(pickup_time):

    summer = [6, 7, 8]
    if pickup_time.month in summer:
        return True
    else:
        return False

def afterUber(pickup_time):
    if (pickup_time.year >= 2011):
        return True
    else:
        return False


def isFourthOfJuly(pickup_time):
    if (pickup_time.month == 7) and (pickup_time.day == 4):
        return True
    else:
        return False

def combiner(line):
    line = line.strip()
    pickup_time, rest = line.split('\t', 1)

    if pickup_time:
        try:
            pickup_time = datetime.strptime(pickup_time, format)

        except ValueError:
            pickup_time = datetime.strptime('2000-02-02 02:02:02', format)

    if isChristmas(pickup_time):
        return('%s\t%s' % ('christmas', rest))

    elif isSummer(pickup_time):
        if isFourthOfJuly(pickup_time):
            return('%s\t%s' % ('summer-julyfourth', rest))
        else:
            return('%s\t%s' % ('summer', rest))

    elif isValentines(pickup_time):
        return('%s\t%s' % ('valentines', rest))

    elif isNewYears(pickup_time):
        return('%s\t%s' % ('newyears', rest))

    elif isLaborDay(pickup_time):
        return ('%s\t%s' % ('laborday', rest))

    elif isMemorialDay(pickup_time):
        return ('%s\t%s' % ('memorialday', rest))


    else:
        return('%s\t%s' % ('noholiday', rest))


for line in sys.stdin:
    line = line.strip()
    data = line.split(',')

    fare_amount = None
    total_amount = None

    if len(data) not in [17, 18, 19, 20, 21]:
        continue

    pickup_time = data[1]

    if len(data) == 17:
        fare_amount = data[10]
        total_amount = data[16]
        distance = data[4]

    elif len(data) == 18:
        fare_amount = data[12]
        total_amount = data[17]
        distance = data[4]

    elif len(data) == 19:
        if '.' in data[5]:
            fare_amount = data[12]
            total_amount = data[18]
            distance = data[4]
        else:
            fare_amount = data[9]
            total_amount = data[16]
            distance = data[8]

    elif (len(data) == 20) or (len(data) == 21):
        fare_amount = data[11]
        total_amount = data[17]
        distance = data[10]


    if fare_amount and total_amount and pickup_time:
        if pickup_time[0].isdigit():
            data = ('%s\t%s&%s' % (pickup_time, fare_amount, 1))
            print(combiner(data))
