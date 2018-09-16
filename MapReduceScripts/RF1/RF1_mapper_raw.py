#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import datetime


#init

# Date Format YYYY-MM-DD hh:mm:ss
format = '%Y-%m-%d %H:%M:%S'
inTimeFrame = False
hour = None
start = 10
end = 11



for line in sys.stdin:

    line = line.strip()
    data = line.split(',')
    data_lenght = len(data)
    pickupTime = None
    destination = None

    if data_lenght in [3, 5, 17, 18, 19, 20, 21]:
            pickupTimeStr = data[1]
            if pickupTimeStr[0].isdigit():
                pickupTime = pickupTimeStr
    else:
        #print('discarding' + str(data_lenght))
        continue

    if (data_lenght in [5, 17, 19]):

        if (data_lenght == 5):
            destination = data[4]

        elif (data_lenght == 17):
            destination = data[8]

        elif (data_lenght == 19):  # More than one type of header has this length
            # Checks that is not a coordinate (lattitude or longitud)
            if ('.' in data[6] or data[6] == 0):
                destination = None
            else:
                destination = data[6]

    if pickupTime:
        pickupTime = datetime.strptime(pickupTime, format)
        hour = pickupTime.hour
        if (start <= hour) and (hour <= end):
            inTimeFrame = True
    else:
        hour = None

    if destination and hour and inTimeFrame:
        print('%s\t%s' % (destination, 1))