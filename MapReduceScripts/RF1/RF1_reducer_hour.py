#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana
'''

import sys

def makeHourDict():
    i = 1
    hours_dict = {}
    while i < 24:
        hours_dict[i] = []
        i += 1

    return hours_dict

def destinationByHour(hours_dict):

    for line in sys.stdin:
        line = line.strip()
        line_length = line.split('\t')

        if len(line_length) == 2:
         hour, destination = line.split('\t', 1)
         hour = int(hour)

        else:
         continue


        hours_dict[hour].append(destination)

    return hours_dict

def countDestination(destination_list):
    counted_list = []
    count = 1
    i = 0

    while i < (len(destination_list) - 1):
        if destination_list[i] == destination_list[i + 1]:
            count += 1
        else:
            counted_list.append('%s\t%s' % (destination_list[i], count))
            count = 1
        i += 1
    counted_list.append('%s\t%s' % (destination_list[i], count))
    return counted_list

def reducer():
    hours_dict = makeHourDict()
    final_dict = makeHourDict()
    destinationByHour_dict = destinationByHour(hours_dict)
    i = 1

    while i < 24:
        counted_destination_list = countDestination(destinationByHour_dict[i])
        final_dict[i] = counted_destination_list
        i += 1

    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        print('%s\t%s' % (1, final_dict[i]))

reducer()