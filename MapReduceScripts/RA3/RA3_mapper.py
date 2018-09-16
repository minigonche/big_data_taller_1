#!/usr/bin/env python
# coding=utf-8

import sys


for line in sys.stdin:
    line = line.strip()
    data = line.split(',')

    fare_amount = None
    total_amount = None
    distance = None

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


    if fare_amount and total_amount and distance and pickup_time:
        if pickup_time[0].isdigit():
            print('%s\t%s&%s' % (pickup_time, fare_amount, 1))
