#!/usr/bin/env python

import sys

import fileinput # import this to read multiple files

for dataLine in fileinput.input():
    dataLine=dataLine.strip()# removing pre and after unnecessary space
    if((not dataLine.isspace()) and dataLine!='' ): # in case we want to avoid space lines / but I handle it in second part as well
    	print(dataLine+'\n') #simply this lien to reducer
