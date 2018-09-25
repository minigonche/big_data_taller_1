#!/usr/bin/env python
# coding=utf-8
"""RF2_mapper.py"""
import sys
import re
from datetime import datetime
# Mapper for header constructor

import random


tag = random.randint(1,1000000)

for line in sys.stdin:
    
	line = line.strip()
	print('%s\t%s' % (tag,1))


            


