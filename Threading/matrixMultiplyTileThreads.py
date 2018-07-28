# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:53:22 2017

@author: JUNAID AHMED GHAURI 
"""

import threading
import time
import numpy as np

 


def multiplyTwoMatrixParallelMethod(loadInt,ThreadId,currentTotalThread,M,mNr): # parallel approach
    lowerRowIndex=ThreadId*loadInt
    upperRowIndex=(ThreadId+1)*loadInt
               
    if ((len(M)%currentTotalThread!=0) and (ThreadId==currentTotalThread-1)):
        upperRowIndex=len(M)-1  # this portion of code is to handle unequal chunks of array that not divide equally in threads 
    
    sumRowColMul=0
    for i in range(lowerRowIndex,upperRowIndex):
        for j in range(0,len(M)-1):
            sumRowColMul=0
            for k in range(0,len(M)-1):
                sumRowColMul=sumRowColMul+(M[i][k]*M[k][j])
            allresults[mNr-1][i][j]=sumRowColMul  
            
  
def multiplyTwoMatrixTiledMethod(loadInt,ThreadId,currentTotalThread,M,mNr): # tiled sequential approach
    lowerRowIndex=ThreadId*loadInt
    upperRowIndex=(ThreadId+1)*loadInt
               
    if ((len(M)%currentTotalThread!=0) and (ThreadId==currentTotalThread-1)):
        upperRowIndex=len(M)-1  # this portion of code is to handle unequal chunks of array that not divide equally in threads 
    
    sumRowColMul=0
    sqrtOfMSize=np.sqrt(len(M))
    rows=len(M)   # we know row and column number are equal
    for i in range(lowerRowIndex,upperRowIndex-1,sqrtOfMSize):
        for j in range(0,rows-1,sqrtOfMSize):
            for k in range(0,rows-1,sqrtOfMSize):
                 for i2 in range(i,min(rows-1,i+sqrtOfMSize)):
                     for j2 in range(j,min(rows-1,j+sqrtOfMSize)):
                        sumRowColMul=0
                        for k2 in range(k,min(rows-1,k+sqrtOfMSize)):
                            sumRowColMul=sumRowColMul+(M[i2][k2]*M[k2][j2])
                        allresults[mNr-1][i2][j2]=allresults[mNr-1][i2][j2]+sumRowColMul 
                
    
        
        
def matrixMultiplicationParallelMethodWithNThreads(M,mNr,argNThread):  # (part a ) this is for parallel multiplication
    # in this task I multiply n x n matrix with itself for experiment purpose
                                                  
    threadsForParallelMethod = [] # array of all threads in current method
    startTimeForParallelMethod=time.time()
    # here multiple thread divide rows of this matrices (one thread process only spcific portion of threads)
    length=len(M)               
    for i in range(argNThread):
        t=threading.Thread(target=multiplyTwoMatrixParallelMethod,args=(int(length/argNThread),i,argNThread,M,mNr,))
        t.start() 
        threadsForParallelMethod.append(t)
    for th in threadsForParallelMethod:
        th.join()
    print("Matrix size: "+str(len(M))+" x "+str(len(M))+" for Matirx Parallel Multiplication operation with: "+str(argNThread)+" number of threads => total time is: "+str(time.time()-startTimeForParallelMethod))
        
def matrixMultiplicationTiledMethodWithNThreads(M,mNr,argNThread):  # (part b )this is for tiled approach multiplication
    # in this task I multiply n x n matrix with itself for experiment purpose
                                                  
    threadsForParallelMethod = [] # array of all threads in current method
    startTimeForParallelMethod=time.time()
    # here multiple thread divide rows of this matrices (one thread process only spcific portion of threads)
    length=len(M)               
    for i in range(argNThread):
        t=threading.Thread(target=multiplyTwoMatrixParallelMethod,args=(int(length/argNThread),i,argNThread,M,mNr,))
        t.start() 
        threadsForParallelMethod.append(t)
    for th in threadsForParallelMethod:
        th.join()
    print("Matrix size: "+str(len(M))+" x "+str(len(M))+" for Matirx Tiled approach Multiplication operation with: "+str(argNThread)+" number of threads => total time is: "+str(time.time()-startTimeForParallelMethod))
      

def main():
    # Main Execution starts from here
    
#=========These 3 loop perform Matrix multiplicatoin with all three different size  with P(nThreadArray) number of threads and caculate the burn time================================#
    for t in nThreadArray: #
        startTime=time.time()    # at the begining of each function set start time to reset to calculate new burn time
        matrixMultiplicationParallelMethodWithNThreads(m1,1,t+1)
    for t in nThreadArray: #
        startTime=time.time()    # at the begining of each function set start time to reset to calculate new burn time
        matrixMultiplicationParallelMethodWithNThreads(m2,2,t+1)
    for t in nThreadArray: #
        startTime=time.time()# at the begining of each function set start time to reset to calculate new burn time
        matrixMultiplicationParallelMethodWithNThreads(m3,3,t+1)
#==========================================#
# now running tiled approadch function with 1 thread
    for t in nThreadArray: #
        startTime=time.time()   # at the begining of each function set start time to reset to calculate new burn time
        matrixMultiplicationTiledMethodWithNThreads(m1,1,t+1)
    for t in nThreadArray: #
        startTime=time.time()   # at the begining of each function set start time to reset to calculate new burn time
        matrixMultiplicationTiledMethodWithNThreads(m2,2,t+1)
    for t in nThreadArray: #
        startTime=time.time()   # at the begining of each function set start time to reset to calculate new burn time
        matrixMultiplicationTiledMethodWithNThreads(m3,3,t+1)
#==========================================#
nThreadStr = input("Enter Max Number of threads: ")  # t o t a l number o f t h r e a d s
nThread=int(nThreadStr)
sizeM1 = int(input("Enter size for 1st Matrix: "))
sizeM2 = int(input("Enter size for 2nd Matrix: "))
sizeM3 = int(input("Enter size for 3rd Matrix: "))
nThreadArray=np.arange(nThread)
  
startTime=time.time()

lock1 = threading.Lock()  # in case of any portion need lock ofr sahred area
lock2 = threading.Lock()


m1 = np.random.randint(9, size=[sizeM1,sizeM1]) #a matrix of nxn random numbers 1-9

m2 = np.random.randint(9, size=[sizeM2,sizeM2]) #a matrix of nxn random numbers 1-9

m3 = np.random.randint(9, size=[sizeM3,sizeM3]) #a matrix of nxn random numbers 1-9

resultMatrix1=np.empty([sizeM1,sizeM1],int)
resultMatrix2=np.empty([sizeM2,sizeM2],int)
resultMatrix3=np.empty([sizeM3,sizeM3],int)

allresults=[]

allresults.append(resultMatrix1)
allresults.append(resultMatrix2)
allresults.append(resultMatrix3)

ThreadId=0
    
    
  
if __name__ == '__main__':
    main()
    
    
