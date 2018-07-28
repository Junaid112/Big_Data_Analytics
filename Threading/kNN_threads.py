# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 03:47:06 2017

@author: JUNAID AHMED GHAURI
"""

import math as mth
import numpy as np
import time
import threading
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity # we can use builtin cosSimilarity as well 

def cosineSim(dt1,dt2):
    cosSim=0.0
    sumdtt1xdt2=0
    sumdtt1xdt1=0
    sumdtt2xdt2=0
    for i in range(len(dt1)-1):
        sumdtt1xdt2=sumdtt1xdt2+dt1[i]*dt2[i]
    for i in range(len(dt1)-1):
        sumdtt1xdt1=sumdtt1xdt1+dt1[i]*dt1[i]
    for i in range(len(dt2)-1):
        sumdtt2xdt2=sumdtt2xdt2+dt2[i]*dt2[i]
        
    cosSim=sumdtt1xdt2/(mth.sqrt(sumdtt1xdt1)*mth.sqrt(sumdtt2xdt2))
    return cosSim

def findSimilarityWithInChunk(threadId,currentTotalThread,trainSet,testV):
    size=len(trainSet)
    allSimilarities=[]
    global result
    for i in range(size):
         allSimilarities.append(cosineSim(trainSet[i],testV))
    maximum=max(allSimilarities)
    result[1]=np.argmax(allSimilarities)*threadId 
    
    if maximum>result[0]:
        result[0]=maximum
        result[1]=np.argmax(allSimilarities)*threadId    
        
        
def KNN_With_NThreads_K_1(trainingDt,testV,argNThread):
    
    threadsForAddition = []
    length=len(trainingDt)
    #startTimeForAddition=time.time()
    chunkSize=int(length/argNThread)
    for i in range(argNThread):
        lowerIndex=i*chunkSize
        upperIndex=(i+1)*chunkSize
               
        if ((length%argNThread!=0) and (i==argNThread-1)):
            upperIndex=length-1
        t=threading.Thread(target=findSimilarityWithInChunk,args=(i,argNThread,trainingDt[lowerIndex:upperIndex],testV))
        t.start() 
        threadsForAddition.append(t)
    for th in threadsForAddition:
        th.join()
    

   
    
result=[0,0] # global variable
    
def main():
    
    sizeTrn = int(input("Enter size of training set (how many members): "))
    sizeVtr = int(input("Enter size of one vector (object): "))
  
    TrainingMatrix=np.random.randint(9, size=[sizeTrn,sizeVtr])
    testVector=np.random.randint(9, size=sizeVtr)
    
    nThreads = int(input("Enter sumber of threads (how many threads: "))
    startTime=time.time()
    
    KNN_With_NThreads_K_1(TrainingMatrix,testVector,nThreads)
    
    burnTime=time.time()-startTime
    
    print ("The Maximum cosineSimilarity is: "+str(result[0])+
    " and the max similarity training observation is at index : "+str(result[1]))
    print ("The total burn time is: "+str(burnTime))  
    
    # I observe this data by runing this program with dirrerent threads
    # now I am going to plot a line graph to demonstrate difference`
    # for matrix size 10000 x 100 (train data)and a vector for test 1 x 100
    # & data for 10500 x 100 as well to see difference
    nThreadOnX=[1,5,50,100]
    timeForKNN10_4=[2.334548234939575,2.2845146656036377,2.2725024223327637,2.2590644359588623]
    timeForKNN10_5=[2.375084638595581, 2.343829870223999,2.3750805854797363,2.4386260509490967]
                
    plt.plot(nThreadOnX,timeForKNN10_4,label='size: 10000 x 100')
    plt.plot(nThreadOnX,timeForKNN10_5,label='size: 10500 x 100')
    plt.ylabel('Time consumed KNN  10^4 x 10^2 Matrix (Training), 1 x 10^2 for Test')
    plt.xlabel('Number of threads')
    plt.legend()
    plt.show()
    
main()