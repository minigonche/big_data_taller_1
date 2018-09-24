#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana
'''



import sys

def makeDayDict():
    #Monday is 0 and Sunday is 6
    i = 0
    day_dict = {}
    while i < 7:
        day_dict[i] = []
        i += 1

    return day_dict

def demandByDay(day_dict):

    for line in sys.stdin:
        line = line.strip()
        line_length = line.split('\t')

        if len(line_length) == 4:
            day, PUlocation = line.split('\t', 1) #PUlocation includes hour

            day = int(day)


        else:
         continue


        day_dict[day].append(PUlocation)

    return day_dict

def countDemand(PUlocation_list):
    counted_list = []
    count = 1
    i = 0

    if len(PUlocation_list) > 0:
        while i < (len(PUlocation_list) - 1):
            if PUlocation_list[i] == PUlocation_list[i + 1]:
                count += 1
            else:
                counted_list.append('%s\t%s' % (PUlocation_list[i], count))
                count = 1
            i += 1

        counted_list.append('%s\t%s' % (PUlocation_list[i], count))
    return counted_list

def reducer():
    day_dict = makeDayDict()
    final_dict = makeDayDict()
    demandByDay_dict = demandByDay(day_dict)
    i = 0

    while i < 7:
        counted_PUlocation_list = countDemand(demandByDay_dict[i])
        final_dict[i] = counted_PUlocation_list
        i += 1

    for i in [0, 1, 2, 3, 4, 5, 6]:
        day_list = ['Mon', 'Tue', 'Wed', 'Thru', 'Fri', 'Sat', 'Sun']
        print('%s\t%s' % (day_list[i], final_dict[i]))

reducer()