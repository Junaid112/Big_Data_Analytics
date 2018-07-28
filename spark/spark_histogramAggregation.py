#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark import SparkContext
import numpy as np
import cv2
import matplotlib.pyplot as plt
from pyspark.sql import SQLContext
from pyspark.sql.functions import min, avg,sum



spark = SparkSession \
    .builder \
    .appName("e8_1") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc=spark.sparkContext
sqlContext = SQLContext(sc)

imageName='cloud.jpg'
maxscale=256	
arOfFrequenciesGrey=np.zeros(maxscale,int)

imgGrey = cv2.imread(imageName,cv2.IMREAD_GRAYSCALE)
oneDAray=np.array(imgGrey).ravel()
rddImage=sc.parallelize(oneDAray)
pairs=rddImage.map(lambda x:(int(x),1))
#listImage=pairs.collect()
# my sequence function is: lambda key,val: key+val
# my combination funciton is: lambda val1, val2: val1+val2
allCountsGrey = pairs.aggregateByKey(0,lambda key,val: key+val, lambda val1, val2: val1+val2).collect()
for x in allCountsGrey:
	arOfFrequenciesGrey[x[0]]=x[1]
	
indexesOdValues=np.arange(0,256)
plt.plot(indexesOdValues,arOfFrequenciesGrey,label="Graph for GreyScale frequencies",color='k')
plt.ylabel('Value from 0 -- 256')
plt.xlabel('Frequncies against each value')
plt.legend()
plt.show()

#############
# below part is for color RGB image histogram
imgRGB = cv2.imread(imageName)
blueM=imgRGB[:,:,0]
greenM=imgRGB[:,:,1]
redM=imgRGB[:,:,2]

oneDArayBlue=np.array(blueM).ravel()
oneDArayGreen=np.array(greenM).ravel()
oneDArayRed=np.array(redM).ravel()


rddImageBlue=sc.parallelize(oneDArayBlue)
rddImageGreen=sc.parallelize(oneDArayGreen)
rddImageRed=sc.parallelize(oneDArayRed)

pairPaintBlue=rddImageBlue.map(lambda x:(int(x),1))
allCountsBlue = pairPaintBlue.aggregateByKey(0,lambda key,val: key+val, lambda val1, val2: val1+val2).collect()

pairPaintGreen=rddImageGreen.map(lambda x:(int(x),1))
allCountsGreen = pairPaintGreen.aggregateByKey(0,lambda key,val: key+val, lambda val1, val2: val1+val2).collect()

pairPaintRed=rddImageRed.map(lambda x:(int(x),1))
allCountsRed = pairPaintRed.aggregateByKey(0,lambda key,val: key+val, lambda val1, val2: val1+val2).collect()

arOfFrequenciesRGB=np.zeros([256,3],int)
for x in allCountsBlue:
	arOfFrequenciesRGB[x[0]][0]=x[1]
for x in allCountsGreen:
	arOfFrequenciesRGB[x[0]][1]=x[1]
for x in allCountsRed:
	arOfFrequenciesRGB[x[0]][2]=x[1]
plt.plot(indexesOdValues,arOfFrequenciesRGB[:,2],label="Graph for 1st dimention colour",color='r')
plt.plot(indexesOdValues,arOfFrequenciesRGB[:,1],label="Graph for 2nd dimention colour",color='g')
plt.plot(indexesOdValues,arOfFrequenciesRGB[:,0],label="Graph for 3rd dimention colour",color='b')
plt.ylabel('Value from 0 -- 256')
plt.xlabel('Frequncies against each value')
plt.legend()
plt.show()
