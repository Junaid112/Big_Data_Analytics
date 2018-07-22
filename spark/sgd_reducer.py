# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 19:35:34 2017

@author: JUNAID
"""


import sys


updatedParamvalue=0

dictinaryOfPartialParameters={}

for data in sys.stdin:
    
    data = data.strip()
    nodeNumebr,partialParamUpdated = data.split("\t",1) # this part is slicing the data which coming from mapper into orignal and predicted
    if(nodeNumebr not in dictinaryOfPartialParameters):
        dictinaryOfPartialParameters[nodeNumebr]=partialParamUpdated
    else:
        dictinaryOfPartialParameters[nodeNumebr]=dictinaryOfPartialParameters[nodeNumebr]+partialParamUpdated
    
    
#at the end this dictionalry contain all updated partial parameters now we have to average them all

sumOfAllPartialParams=0

for x in dictinaryOfPartialParameters:
    sumOfAllPartialParams=sumOfAllPartialParams+dictinaryOfPartialParameters[x]
    
averageUpdatedParameter=sumOfAllPartialParams/len(dictinaryOfPartialParameters) # it means that many nodes we have
print("final average Updated Parameter from all nodes is: ", averageUpdatedParameter)
