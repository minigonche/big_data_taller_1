#!/usr/bin/env python
# coding=utf-8


import sys

total_count = 0
holiday_count = 0
current_holiday = None
holiday_cost = 0
total_cost = 0

for line in sys.stdin:
    line = line.strip()
    holiday, rest = line.split('\t', 1)
    cost, count = rest.split('&', 1)


    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # convert count (currently a string) to int
    try:
        cost = float(cost)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_holiday == holiday:
        holiday_count += count
        holiday_cost += cost
    else:
        if current_holiday:
            # write result to STDOUT
            holiday_average = holiday_cost / holiday_count
            print('%s\t%s\t%s\t%s' % (current_holiday, holiday_cost, holiday_count, holiday_average))
        holiday_count = count
        holiday_cost = 0
        holiday_average = 0
        current_holiday = holiday

    total_count += 1
    total_cost += cost

# do not forget to output the last word if needed!
if current_holiday == holiday:
    holiday_average = holiday_cost / holiday_count
    print('%s\t%s\t%s\t%s' % (current_holiday, holiday_cost, holiday_count, holiday_average))

total_average =  total_cost / total_count

print('%s\t%s\t%s\t%s' % ('total', total_cost, total_count, total_average))