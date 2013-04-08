#!/usr/bin/env python
import numpy
from numpy import *
import math
import scipy
import sys
import csv


fName = sys.argv[1]
outName = sys.argv[2]
fr = open(fName)
content = [line.strip() for line in fr.readlines()]
metrics_content = content[1:][:]
metrics1 = [a.split(",")[1:] for a in metrics_content]
fr.close()

fr = open(outName)
content = [line.strip() for line in fr.readlines()]
metrics_content = content[1:][:]
metrics2 = [a.split(",")[1:] for a in metrics_content]
fr.close()

datArr1 = [map(float,val) for val in metrics1]
datArr2 = [map(float,val) for val in metrics2]

matrx1 = mat(datArr1)
matrx2 = mat(datArr2)

fp = open(fName)
line = fp.readline()
firstLine = line.strip().split(',')
content = [line.strip() for line in fp.readlines()]
metrics_content = content[0:][:]
metrics1= [a.split(",")[0] for a in metrics_content]
fp.close()

fp = open(outName)
line = fp.readline()
firstLine = line.strip().split(',')
content = [line.strip() for line in fp.readlines()]
metrics_content = content[0:][:]
metrics2= [a.split(",")[0] for a in metrics_content]
fp.close()

if matrx1.shape[0] != matrx2.shape[0]:
	print "error"
if matrx1.shape[1] != matrx2.shape[1]:
	print "error"

print matrx2[0,0]
error = 0
for i in range(matrx1.shape[0]):
	for j in range(matrx1.shape[1]):
		#print matrx1[i,j]
		#print matrx2[i,j]
		m1= fabs(0.001*fabs(matrx1[i,j]))
		m2= fabs(0.001*fabs(matrx1[i,j]))
		if (fabs(matrx1[i,j] - matrx2[i,j])  > m1) or (fabs(matrx1[i,j] - matrx2[i,j])  > m2):
			if (fabs(matrx1[i,j]) != 0) * (fabs(matrx2[i,j]) != 0):
				print "error value"
				a = fabs(matrx1[i,j] - matrx2[i,j])
				error = 1
				print i,j,a
				print matrx1[i,j]
                		print matrx2[i,j]
				break
		else:
			a = fabs(matrx1[i,j] - matrx2[i,j])
      			#print a
			#print "*******" 
	if error == 1:
		break
	#print metrics1[i]
        if metrics1[i] != metrics2[i] :
		print "ID error"
		break

