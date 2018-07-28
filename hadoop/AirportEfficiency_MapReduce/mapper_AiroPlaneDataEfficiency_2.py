#!/usr/bin/env python

import sys

for line in sys.stdin:
  dataToken = line.strip().split(",")
  if(len(dataToken)>7):
#if we want to know index of related data we can do by read first line and note down the relevent index or 
#we can put it like below at [3] is our airport name and at [8] is Arrival delay
  	(flight,delay) = (dataToken[3],dataToken[8])
	if(delay):
		#we know at 3 index airport_id and last index delayTime
  		print("%s\t%s" % (flight,delay))
