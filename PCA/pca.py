#!/usr/bin/env python
import numpy
from numpy import *
import math
import scipy
import sys
import csv

def loadDataSet(fileName, delim=','):
	fr = open(fileName)
	content = [line.strip() for line in fr.readlines()]
        metrics_content = content[1:][:]
        #print metrics_content
	#metrics = [a.split(delim)[1:-1] for a in metrics_content]
	metrics = [a.split(delim)[1:] for a in metrics_content]
        #print metrics
	#replaceBlankWithMean(metrics)
        datArr = [map(float,val) for val in metrics]
	#print datArr[0]
	#stringArr = [line.strip().split(delim) for line in fr.readlines()]
	#datArr = [map(float,line) for line in stringArr]
	return mat(datArr)

def isBlank(val):
	print val
	return not val

def replaceBlankWithMean(dataMat):
	numFeat = shape(dataMat)[1]
	for i in range(numFeat):
		meanVal = mean(dataMat[nonzero(~isBlank(dataMat[:,i].A))[0],i])
		dataMat[nonzero(isBlank(dataMat[:,i].A))[0],i] = meanVal
	return datMat


def pca(dataMat, topNfeat=9999999):
    	#print dataMat
	meanVals = mean(dataMat, axis=0)
	#stdVals = std(dataMat, axis=0)
	meanRemoved = dataMat - meanVals
	covMat = cov(meanRemoved, rowvar=0)
        #print covMat
	eigVals,eigVects = linalg.eig(mat(covMat))
	#print eigVals
	eigValInd = argsort(eigVals)
	eigValInd = eigValInd[:-(topNfeat+1):-1]
        #print eigValInd
	#print "*********************"
        #print eigVects
	redEigVects = eigVects[:,eigValInd]
	#print "*********************"
        print redEigVects
	#print "*********************"
	lowDDataMat = meanRemoved * redEigVects
	reconMat = (lowDDataMat * redEigVects.T) + meanVals
        #reconMat.tofile("selected_reconstructed.txt", ",", "%s")
	return lowDDataMat, reconMat

def calculateFractionOfVarianceExplainedByPCA(lowDMat):
        PCAcovarMat = cov(lowDMat,rowvar=0)
        #print PCAcovarMat
        retList = []
        matSize = PCAcovarMat.shape[0]
        totalVariance = 0.0
        for d in range(matSize):
              covar = PCAcovarMat[d,d]
              #print covar
              totalVariance += covar
        kk = 0
        for d in range(matSize):
              covar = PCAcovarMat[d,d]
              #print covar
              #kk = kk + covar/4.0
              #print kk
              fraction = covar/totalVariance
              percentageVar = 100*(fraction)
              retList.append(fraction)
              print "Total variance explained by PC",d," is ", percentageVar
        return retList

def testPCA():
	#dataMat = numpy.array([[-1, 1, 2, 2],
        #   [-2, 3, 1, 0],
        #   [ 4, 0, 3,-1]],dtype=double)
        dataMat = numpy.array([[2, 2, -1, 5],
           [1, 0, -2, -3],
           [ 3, -1, 4,0]],dtype=double)

        dataMat = numpy.array([[-1, 5, -1, 5],
           [2,3 , -2, -3],
           [-3, 2, -2, -3],
           [ 4, 1, 4,0]],dtype=double)

	lowDMat, reconMat = pca(dataMat)
        #dataMat[:,1] = dataMat[:,1] * 2
        #dataMat[:,3] = dataMat[:,3] * 5
        print dataMat
	#print lowDMat
        percentagePCA = calculateFractionOfVarianceExplainedByPCA(lowDMat)
        print "***********************************"
	print percentagePCA

def optimizedRankingAlgo(fileName):
        fp = open(fileName)
        line = fp.readline()
        firstLine = line.strip().split(',')
        fp.close()
        #names = numpy.array(firstLine[1:-1])
        names = numpy.array(firstLine[1:])

        #print names.shape
        print names
        dataMat = loadDataSet(fileName)
        #print dataMat
        meanVals = mean(dataMat, axis=0)
        meanRemoved = dataMat - meanVals
        covMat = cov(meanRemoved, rowvar=0)
        print covMat
        eigVals,eigVects = linalg.eig(mat(covMat))
        eigValInd = argsort(eigVals)
        eigValInd = eigValInd[:-(999999+1):-1]
        print eigVals[:,eigValInd]
        redEigVects = eigVects[:,eigValInd]
        #lowDMat, reconMat = pca(dataMat)
        lowDDataMat = meanRemoved * redEigVects
        T = redEigVects.getA()
        print T
        percentagePCA = calculateFractionOfVarianceExplainedByPCA(lowDDataMat)
        for d in range(T.shape[0]):
                T[:,d] = T[:,d] * percentagePCA[d]

        #print T
        rankMatrix = {}
        rank = names.shape[0]
        maxRowMap = {}
        index = 0
        for r in T:
          valMax = numpy.amax(r)
          maxRowMap[index] = valMax
          index = index + 1
        #endfor
        for key, value in sorted(maxRowMap.iteritems(), key=lambda (k,v): (v,k)):
                #print "%s: %s" % (names[key], value)
                rankMatrix[names[key]] = rank
                rank = rank - 1
        print rankMatrix
        return rankMatrix

def rankUsingPCA(fileName):
        fp = open(fileName)
        line = fp.readline()
        firstLine = line.strip().split(',')
        fp.close()
        #names = numpy.array(firstLine[1:-1])
        names = numpy.array(firstLine[1:])

        #print names.shape
        print names
        dataMat = loadDataSet(fileName)
        #print dataMat
        meanVals = mean(dataMat, axis=0)
        meanRemoved = dataMat - meanVals
        covMat = cov(meanRemoved, rowvar=0)
        eigVals,eigVects = linalg.eig(mat(covMat))
        eigValInd = argsort(eigVals)
        eigValInd = eigValInd[:-(999999+1):-1]
        redEigVects = eigVects[:,eigValInd]
        #lowDMat, reconMat = pca(dataMat)
        lowDDataMat = meanRemoved * redEigVects
        T = redEigVects.getA()
        print T
        # calculate the variance covered by each components in PCA
        percentagePCA = calculateFractionOfVarianceExplainedByPCA(lowDDataMat)
        for d in range(T.shape[0]):
                T[:,d] = T[:,d] * percentagePCA[d]

        #print T
        rankMatrix = {}
        rank = 0
        while(T.shape[0] > 1 and T.shape[1] > 1):
                rowMax = -99999
                index = 0
                maxIndex = -1
                for r in T:
                  valMax = numpy.amax(r)
                  if (valMax > rowMax):
                    rowMax = valMax
                    maxIndex = index
                  #endif
                  index = index + 1
                #endfor
                print names[maxIndex]
                rankMatrix[names[maxIndex]] = rank
                rank = rank + 1
                T = scipy.delete(T,maxIndex,0)
                #print T
                names = scipy.delete(names,maxIndex,0)
                #print names
        #end while
        print names[0]
        rankMatrix[names[0]] = rank
        return rankMatrix

def rankMatrixHeuristic(fileName):
	fp = open(fileName)
	line = fp.readline()
	firstLine = line.strip().split(',')
	fp.close()
	#names = numpy.array(firstLine[1:-1])
	names = numpy.array(firstLine[1:])

	#print names.shape
	#print names
	dataMat = loadDataSet(fileName)
        #print dataMat
	meanVals = mean(dataMat, axis=0)
	meanRemoved = dataMat - meanVals
	covMat = cov(meanRemoved, rowvar=0)
	eigVals,eigVects = linalg.eig(mat(covMat))
	eigValInd = argsort(eigVals)
	eigValInd = eigValInd[:-(999999+1):-1]
	redEigVects = eigVects[:,eigValInd]
	#lowDMat, reconMat = pca(dataMat)
        lowDDataMat = meanRemoved * redEigVects

        #Do we need to transpose ??? check!!
	#T = lowDMat.T.getA()
	#T = lowDMat.getA()
        # which one is the correct eigen vector, rows or columns!! verify!!
	T = redEigVects.getA()
	#T = redEigVects.T.getA()
        #print T[0].shape
        #print T.shape
        #print T
	#numpy.savetxt("kk.txt",T,'%.18e'," , ")
	#T = reconMat.T.getA()
	#names = numpy.array(['B','C','D','E'])
        # calculate the variance covered by each components in PCA
        #percentagePCA = calculateFractionOfVarianceExplainedByPCA(lowDDataMat)
        # before using ranking huristic, adjust weights of each components in each PCA by its corresponding percentage
        #for d in range(T.shape[0]):
         #       T[:,d] = T[:,d] * percentagePCA[d]

        #print T
        rankMatrix = {}
	rank = 0
	while(T.shape[0] > 1 and T.shape[1] > 1):
        	k = [math.fabs(r[0]) for r in T]
		#print "k", k
        	j = numpy.argmax(k)
        	#print j
        	#print T.shape
        	#print names.shape
        	print names[j]
                rankMatrix[names[j]] = rank
                rank = rank + 1
        	T = scipy.delete(T,j,0)
		#print T
        	names = scipy.delete(names,j,0)
        	#print T.shape
        	for i in range(0,T.shape[0]):
                	if(T.shape[1] > 1):
				if(math.fabs(T[i,0]) > math.fabs(T[i,1])):
                                	T[i,1] = T[i,0]
        
		T = scipy.delete(T,0,1)
	#end while
	print names[0]
        rankMatrix[names[0]] = rank
	return rankMatrix

def rankBasedOnMaxShiftOfPCA(fname1,fname2):
	#rmtx1 = rankMatrixHeuristic(fname1)
	#rmtx2 = rankMatrixHeuristic(fname2)
	rmtx1 = rankUsingPCA(fname1)
	rmtx2 = rankUsingPCA(fname2)
        diffMtx = {}
	for k1, v1 in rmtx1.iteritems():
		v2 = rmtx2[k1]
		diffMtx[k1] = abs(v1-v2)

	#rint diffMtx     
	print "***Most diverged components in PCA****"  
	for key, value in sorted(diffMtx.iteritems(), key=lambda (k,v): (v,k)):
    		print "%s: %s" % (key, value)

def generateNewFileWithPrincipalComponent(fileName,outFile,numPC):
	fp = open(fileName)
        line = fp.readline()
        firstLine = line.strip().split(',')
	content = [line.strip() for line in fp.readlines()]
        metrics_content = content[0:][:]
	metrics = [a.split(",")[0] for a in metrics_content]
        fp.close()
	#print metrics[6]
        #names = numpy.array(firstLine[1:-1])
        #names = numpy.array(firstLine[1:])
        #print names
        dataMat = loadDataSet(fileName)
        lowDMat, reconMat = pca(dataMat,numPC)
       
        #T = lowDMat.T.getA()
	k = 0
        #T = reconMat.T.getA()
        T = reconMat.getA()
        #T = lowDMat.getA()
        item_length = T.shape[0]
        numPC = T.shape[1]
   
        names = [i for i in range(numPC)]
        names.append(numPC + 1)

        #print item_length
	#print T.shape
	#print names
	#print len(metrics)
	with open(outFile, 'wb') as test_file:
  		file_writer = csv.writer(test_file)
		file_writer.writerow(names)
  		for i in range(item_length):
			#print i
			z = [x for x in T[i]]
			# = [metrics[i],z]
			z.insert(0,metrics[i])
    			file_writer.writerow(z)
        #print T.shape
        #print names.shape
	#toDump = numpy.hstack([names,T])
        #toDump = T
	#numpy.savetxt("/home/mitra4/principal.txt", M)



