#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana

This script sorts data using mergeSort prior to running the reducer
'''

import sys

current_destination = None
current_count = 0
destination = None
data = []
sorted_data = []

def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    return alist

#sort data to imitate hadoop behaviour
for line in sys.stdin:
    line.strip()
    data.append(line)
    sorted_data = mergeSort(data)

for line in sorted_data:

    # remove leading and trailing whitespace
    line = line.strip()
    destination, count = line.split('\t', 1)
    count = int(count)

    if current_destination == destination:
        current_count += count
    else:
        if current_destination:
            current_count += count
            # write result to STDOUT
            print('%s\t%s' % (current_destination, current_count))
            current_count = 0
    current_destination = destination

# do not forget to output the last destination if needed!
if current_destination == destination:
    print('%s\t%s' % (current_destination, current_count))
