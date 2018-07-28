# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:26:49 2017

@author: JUNS
"""



from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

def multiplyMatrix(m1,m2,resultantMatrix,rank,nProcess):
   
    #we  assume that number of columns of first and rows of second matrix are equal, so we can multiply
    for x in range(rank,len(m1),nProcess):
        for y in range(len(m2)):
            resultantMatrix[x][y]=sum(m1[x,:]*m2[:,y]) #this line will multiply row with column and summ on resultant matrix
            
    return resultantMatrix

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    root = 0
    startTime=MPI.Wtime()
    sizeOfMatrix=1000
    
    oprt = MPI.SUM
    np.random.seed(111)
    m1=np.random.randint(9,size=[sizeOfMatrix,sizeOfMatrix])
    np.random.seed(222)
    m2=np.random.randint(9,size=[sizeOfMatrix,sizeOfMatrix])
    resultM=np.zeros([sizeOfMatrix,sizeOfMatrix],int)
    #for this exercise I assume that both matrix are same size, otherwise I can some change if requirement change
    resultM=multiplyMatrix(m1,m2,resultM,rank,size)
    #print(resultM)
    FinalMatrixAfterReduce=comm.reduce(resultM,root=0,op=oprt)
    if(rank==root):
        tTime=MPI.Wtime()-startTime
        print("Matrix are multiplied in total Time: "+str(tTime))
        #print("Resultant Matrix data is is: ")
        #print(FinalMatrixAfterReduce)
        ########################## I've note down some experiment results ans compare in graph on my p.c core to duo 
        nThreadOnX=[1,2,3,4] # these are just my sample experiments I note down
        timeForKNN10_4=[15.2404655,8.0713062,8.2592825,8.3839226]
                     
        plt.plot(nThreadOnX,timeForKNN10_4,label='Time to Multiply Matrix: 10000 x 1000')
        plt.ylabel('Time consumed to compute Multiplication')
        plt.xlabel('Number of Processes using MPI , Matrix size 1000 x 1000')
        plt.legend()
        plt.show()
    
main()
                 