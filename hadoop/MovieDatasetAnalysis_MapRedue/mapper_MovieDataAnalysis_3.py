#!/usr/bin/env python

import sys

for line in sys.stdin:
	dataToken = line.strip().split("::")
	sizeToken=len(dataToken)
	if(sizeToken==3): # now for genere as well
		print("%s=%s=%s=%s" % (dataToken[0],dataToken[1],dataToken[2],"2"))#3rd one is data type what is my input stream from
	elif(sizeToken>3):
		print("%s=%s=%s%s" % (dataToken[1],dataToken[2],"1","0"))
