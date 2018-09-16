#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import datetime
counter = 0


for line in sys.stdin:
    print('line' + str(counter) + ': ' + line)
    counter += 1