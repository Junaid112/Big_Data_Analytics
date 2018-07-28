# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:53:22 2017

@author: JUNAID AHMED GHAURI 
"""

import threading
import time
import numpy as np

 


def addVectorWithItsOwn(loadInt,ThreadId,currentTotalThread,v,vNr): 
   
    global allresult
    
    lowerIndex=ThreadId*loadInt
    upperIndex=(ThreadId+1)*loadInt
               
    if ((len(v)%currentTotalThread!=0) and (ThreadId==currentTotalThread-1)):
        upperIndex=len(v)-1  # this portion of code is to handle unequal chunks of array that not divide equally in threads 
    for i in range(lowerIndex,upperIndex):
        allresults[vNr-1][i]=v[i]+v[i]

def findMinimum(loadInt,ThreadId,currentTotalThread,v,vNr):  
    lowerIndex=ThreadId*loadInt
    upperIndex=((ThreadId+1)*loadInt)-1
    if ((len(v)%currentTotalThread!=0) and (ThreadId==currentTotalThread-1)):
        upperIndex=len(v)-1  # this portion of code is to handle unequal chunks of array that not divide equally in threads 
    
    subV=v[lowerIndex:upperIndex]
    curMin=min(subV)
    if curMin<minArray[vNr-1]:
        minArray[vNr-1]=curMin
    
    
def findAverage(loadInt,ThreadId,currentTotalThread,v,vNr):
    lowerIndex=ThreadId*loadInt
    upperIndex=((ThreadId+1)*loadInt)-1
    if ((len(v)%currentTotalThread!=0) and (ThreadId==currentTotalThread-1)):
        upperIndex=len(v)-1  # this portion of code is to handle unequal chunks of array that not divide equally in threads 
    
    subV=v[lowerIndex:upperIndex]
    sumArray[vNr-1]=sumArray[vNr-1]+sum(subV)

    
    
def additionWithNThreads(v,vNr,argNThread):
    threadsForAddition = []
    length=len(v)
    startTimeForAddition=time.time()
    for i in range(argNThread):
        t=threading.Thread(target=addVectorWithItsOwn,args=(int(length/argNThread),i,argNThread,v,vNr,))
        t.start() 
        threadsForAddition.append(t)
    for th in threadsForAddition:
        th.join()
    print("vector size: "+str(len(v))+" for addition operation with: "+str(argNThread)+" number of threads => total time is: "+str(time.time()-startTimeForAddition))
        

def minimumWithNThreads(v,vNr,argNThread):  
    threadsForMinimum = []
    length=len(v)
    startTimeForMinimum=time.time()
    for i in range(argNThread):
        t2=threading.Thread(target=findMinimum,args=(int(length/argNThread),i,argNThread,v,vNr,))
        t2.start()
        threadsForMinimum.append(t2)
        
    for th in threadsForMinimum:
        th.join()
        
    print("Minimum is: "+str(minArray[vNr-1]))
    print("vector size: "+str(len(v))+" for Minimum operation with: "+str(argNThread)+" number of threads => total time is: "+str(time.time()-startTimeForMinimum))
    
        
def averageWithNThreads(v,vNr,argNThread):  
    threadsForAverage = []
    length=len(v)
    startTimeForAverage=time.time()
    for i in range(argNThread):
        t2=threading.Thread(target=findAverage,args=(int(length/argNThread),i,argNThread,v,vNr,))
        t2.start()
        threadsForAverage.append(t2)
        
    for th in threadsForAverage:
        th.join()
    print("Average is: "+str(sumArray[vNr-1]/len(v)))  
    print("vector size: "+str(len(v))+" for addition operation with: "+str(argNThread)+" number of threads => total time is: "+str(time.time()-startTimeForAverage))
            
    


def main():
    # Main Execution starts from here
    
#=========These 3 loop perform addition with all three different size vectors with P(nThreadArray) number of threads and caculate the burn time================================#
    for t in nThreadArray: #
        startTime=time.time()    # at the begining of each function set start time to reset to calculate new burn time
        additionWithNThreads(v1,1,t+1)
    for t in nThreadArray: #
        startTime=time.time()    # at the begining of each function set start time to reset to calculate new burn time
        additionWithNThreads(v2,2,t+1)
    for t in nThreadArray: #
        startTime=time.time()# at the begining of each function set start time to reset to calculate new burn time
        additionWithNThreads(v3,3,t+1)
#==========================================#

#=========These 3 loop find minimum from all three different size vector separately with P(nThreadArray) number of threads and caculate the burn time================================#    
    for t in nThreadArray: #
        startTime=time.time() # at the begining of each function set start time to reset to calculate new burn time
        minimumWithNThreads(v1,1,t+1)
    for t in nThreadArray: #
        startTime=time.time()# at the begining of each function set start time to reset to calculate new burn time
        minimumWithNThreads(v2,2,t+1)
    for t in nThreadArray: #
        startTime=time.time()# at the begining of each function set start time to reset to calculate new burn time
        minimumWithNThreads(v3,3,t+1)
#=========================================#
        
#=========These 3 loop find average from all three different size vector separately with P(nThreadArray) number of threads and caculate the burn time================================#
        
    for t in nThreadArray: #
        startTime=time.time() # at the begining of each function set start time to reset to calculate new burn time
        averageWithNThreads(v1,1,t+1)
    for t in nThreadArray: #
        startTime=time.time() # at the begining of each function set start time to reset to calculate new burn time
        averageWithNThreads(v2,2,t+1)
    for t in nThreadArray: #
        startTime=time.time() # at the begining of each function set start time to reset to calculate new burn time
        averageWithNThreads(v3,3,t+1)
#=========================================#

nThreadStr = input("Enter Max Number of threads: ")  # t o t a l number o f t h r e a d s
nThread=int(nThreadStr)
sizeV1 = int(input("Enter size for 1st vector: "))
sizeV2 = int(input("Enter size for 2nd vector: "))
sizeV3 = int(input("Enter size for 3rd vector: "))
nThreadArray=np.arange(nThread)
  
startTime=time.time()

lock1 = threading.Lock()  # in case of any portion need lock ofr sahred area
lock2 = threading.Lock()


v1 = np.random.randint(9, size=sizeV1) #a list of provided random numbers 1-9

v2 = np.random.randint(9, size=sizeV2) #a list of provided random numbers 1-9

v3 = np.random.randint(9, size=sizeV3) #a list of provided random numbers 1-9

allresults=[]
result1 = np.empty([sizeV1],int) # for addition operation result vector
result2 = np.empty([sizeV2],int) #for addition operation result vector 
result3 = np.empty([sizeV3],int) #for addition operation result vector


allresults.append(result1)
allresults.append(result2)
allresults.append(result3)

minArray=np.empty([3],int)
sumArray =np.empty([3],int)
ThreadId=0
    
    
  
if __name__ == '__main__':
    main()
    
    
