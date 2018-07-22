# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 19:35:06 2017

@author: JUNAID
"""

import sys
partialUpdtedParameter=0

for inputdata in sys.stdin: # read data from input stream , each line contain orignal value and predicted value with tab separated
    Y,yHat=inputdata.split("\t").strip()# remove   unnecessary spaces before and after
    # now input contain y and yHat as well
    partialUpdtedParameter=sgd(Y,yHat) # updation in parameter for perticulat point subset
    print("%s\t%s" % (nodeNumber,partialUpdtedParameter)) #bith data points are mapped twards reducer