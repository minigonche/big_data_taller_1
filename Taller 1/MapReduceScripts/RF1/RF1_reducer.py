#!/usr/bin/env python
# coding=utf-8

'''
Reto 1: Encuentre cuál es el sitio de la ciudad hacia el cual se dirigen la mayor cantidad de vehículos en una cierta
franja de horas del día, para cada día de la semana
'''

import sys

current_destination = None
current_count = 0
destination = None

for line in sys.stdin:

    # remove leading and trailing whitespace
    line = line.strip()
    line_length = line.split('\t')

    if len(line_length) == 2:
        destination, count = line.split('\t', 1)
    else:
        continue

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
