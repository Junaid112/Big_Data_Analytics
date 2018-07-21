
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 20:38:03 2017

@author: JUNAID
"""



from mpi4py import MPI
import numpy
import time


def computeChunkDot(v1,v2):
    sumOfDot=0
    for i in range(len(v1)):
        sumOfDot=sumOfDot+(v1[i]*v2[i])
    return sumOfDot

    
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
root = 0

op = MPI.SUM
# let suppose vector size n so for two vector dot prod my program sahpe a matrix of 2 x n(each row is vector)
#n=1000...now we have 2 vector means (2 x n matrix can be shaped)
if rank==root:
    startTime=time.time() #split matrix horizontally so each process have equal part of both vectors
    numOfProcess=5
    dataToScatter=numpy.hsplit(numpy.random.randint(9,size=[2,1000000]),numOfProcess)
else:
    dataToScatter=None
recvdata=comm.scatter(dataToScatter,root=root)
dotForEachSlice=computeChunkDot(recvdata[0],recvdata[1])
recSumOfDot=numpy.empty(1,dtype=int)
comm.Reduce(dotForEachSlice,recSumOfDot,root=root,op=op)

if rank==root:
    print("By running this program with: {} processes dotProduct of Two Vectors is: {}"
      . format (size,recSumOfDot[0]))
    print("Run time is : "+str(time.time()-startTime)+" second")



##############For sequence ru and time comparison #############################
#startTime=time.time()
#v=numpy.random.randint(9,size=[1000000])
#r=computeChunkDot(v,v)
#print("result: "+str(r)+"  in time: "+str(time.time()-startTime)+" seconds")
###############################################################################
    import matplotlib.pyplot as plt
    sizeOfVector=[100000,1000000,10000000]
    timeForParallelProcess=[0.0519876,0.565371,5.558745]
    timeForSequential=[0.079052,0.786745,7.764756]
                
    plt.plot(sizeOfVector,timeForParallelProcess,label='For parallel multiProcess')
    plt.plot(sizeOfVector,timeForSequential,label='For sequental Program')
    plt.ylabel("Time consumed by for dotproduct by parallel vs Sequential")
    plt.xlabel("Size of vectors")
    plt.legend()
    plt.show()
#    
#########################################################