#!/usr/bin/env python
# coding=utf-8


import sys
from datetime import datetime

format = '%Y-%m-%d %H:%M:%S'


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


for line in sys.stdin:
    line = line.strip()
    pickup_time, rest = line.split('\t', 1)

    if pickup_time:
        try:
            pickup_time = datetime.strptime(pickup_time, format)

        except ValueError:
            pickup_time = datetime.strptime('2000-02-02 02:02:02', format)

    if isChristmas(pickup_time):
        print('%s\t%s' % ('christmas', rest))

    elif isSummer(pickup_time):
        if isFourthOfJuly(pickup_time):
            print('%s\t%s' % ('summer-julyfourth', rest))
        else:
            print('%s\t%s' % ('summer', rest))

    elif isValentines(pickup_time):
        print('%s\t%s' % ('valentines', rest))

    elif isNewYears(pickup_time):
        print('%s\t%s' % ('newyears', rest))

    else:
        print('%s\t%s' % ('noholiday', rest))


