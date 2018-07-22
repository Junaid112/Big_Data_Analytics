# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 19:34:33 2017

@author: JUNAID
"""

from mpi4py import MPI
import numpy as np


def estimateParameterOFrDataPart(Y,yHat,paramenterval,rank,size):
    
    # below loop only access relevent index, this is how data is divided among allprocesses
    updatedParamvalue=0
    for i in range(rank,len(Y),size):
        updatedParamvalue=updatedParamvalue+ sgd(Y[i],yHat[i]) # updation in parameter for perticulat point subset
    
    return updatedParamvalue
    
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
root = 0
finalResultanParameter=0
totalDataPoints=1000 #let supose
#eacg poit has 2 dimention x and y
dimention=2
# here we generate orignal data points
Y=np.random.randint(9, size=[dimention,totalDataPoints])

# let supoose some algorithm gave us the new predicted points in array yHat
yHat=np.random.randint(9, size=[dimention,totalDataPoints])
paramenterval=np.random.randint(10)# some randon initialization for parameter

####################
updatedParameter=estimateParameterOFrDataPart(Y,yHat,rank,size)

oprt = MPI.SUM # because at end we need to take aaverage from all updations
comm.Reduce(updatedParameter,finalResultanParameter,root=root,op=oprt)
    
if(rank==root):
    averageUpdatedParameter=finalResultanParameter/size
    print("Final average updated parameter from all process using MPI is: ", averageUpdatedParameter)
    
    
    
    
    
    
    
    