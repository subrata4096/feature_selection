#!/usr/bin/env python
import numpy
from numpy import *
import math
import scipy
import sys
import csv


fName = sys.argv[1]
fp = open(fName)
line = fp.readline()
firstLine = line.strip().split(',')
content = [line.strip() for line in fp.readlines()]
metrics_content = content[0:][:]
metrics1= [a.split(",")[0] for a in metrics_content]
fp.close()
unique_class = {}
n = len(metrics1)
for i in range(n):
        id = metrics1[i]
        #print id
        #id = 'ENTER-hhh/hhhj/hhgg/wdcg/hhjjkl/abc$hjrtl'
        a = 1 + id.rfind('/')
        b = id.find('$')
        new_id = id[a:b]
        #print new_id
        unique_class[new_id] = 1
#print unique_class
print len(unique_class)
