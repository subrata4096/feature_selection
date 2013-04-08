#!/usr/bin/env python
import numpy
import math
import scipy
import sys
import pca

fName = sys.argv[1]
outName = sys.argv[2]
#pca.testPCA()
#pca.rankMatrixHeuristic(fName)
#pca.rankUsingPCA(fName)
#pca.optimizedRankingAlgo(fName)
pca.rankBasedOnMaxShiftOfPCA(fName,outName)
#pca.generateNewFileWithPrincipalComponent(fName,outName,15)


