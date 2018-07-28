# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:26:49 2017

@author: JUNS
"""



from mpi4py import MPI
import numpy as np
from decimal import *

def calculatePiValue(precision,rank,nProcess):
    getcontext().prec = precision
    piVal=Decimal(0)
    
    for i in range(rank,precision,nProcess):
        piVal=piVal+Decimal(((1/16**i)*((4/(8*i+1))-(2/(8*i+4))-(1/(8*i+5))-(1/(8*i+6)))))
    return piVal

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    root = 0
    startTime=MPI.Wtime()
    #you can change precision size according to how many digit you want after decimal n+1 (1 for 3 before decimal)
    precision=1001 # because forst one will be before the decimal point that's why 1+1000
    
    
    piValue=calculatePiValue(precision,rank,size)
    oprt = MPI.SUM
    resultant=comm.reduce(piValue,root=0,op=oprt)
    if(rank==root):
        
        print("Pi value computed is: "+str(resultant))
        finalTime=MPI.Wtime()-startTime
        print("Total time consumed: "+str(finalTime))
    
main()
                 