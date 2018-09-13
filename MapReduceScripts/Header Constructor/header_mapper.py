#!/usr/bin/env python
# coding=utf-8
"""RF2_mapper.py"""
import sys
import re
from datetime import datetime
# Mapper for header constructor


for line in sys.stdin:
    
    if('_' in line):
        line = line.strip()
        print('%s\t%s' % (line,1))


            


