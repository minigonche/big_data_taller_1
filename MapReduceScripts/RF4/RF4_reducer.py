#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana
'''



import sys

def makeMonthDict():
    i = 1
    month_dict = {}
    while i < 13:
        month_dict[i] = []
        i += 1

    return month_dict

def demandByMonth(month_dict):

    for line in sys.stdin:
        line = line.strip()
        line_length = line.split('\t')

        if len(line_length) == 3:
            month, PUlocation = line.split('\t', 1) #PUlocation includes hour
            month = int(month)

        else:
         continue


        month_dict[month].append(PUlocation)

    return month_dict

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
    month_dict = makeMonthDict()
    final_dict = makeMonthDict()
    demandByMonth_dict = demandByMonth(month_dict)
    i = 1

    while i < 13:
        counted_PUlocation_list = countDemand(demandByMonth_dict[i])
        final_dict[i] = counted_PUlocation_list
        i += 1



reducer()