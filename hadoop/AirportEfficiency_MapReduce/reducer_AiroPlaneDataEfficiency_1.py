#!/usr/bin/env python

#from operator import itemgetter
import sys

#below two line airport name and temporary name for compare
airportId=""
tempAirportId=""

delayTime=-0.0
minTime=-0.0
maxTime=-0.0
sumTime=0.0
countInst=0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    #print(line.split("\t",1))
    # parse the input we got from mapper
    airportIdstr, delayTimestr = line.split("\t",1)

    try:
        tempAirportId = airportIdstr
	delayTime=float(delayTimestr)
	if (airportId==""):
		airportId=tempAirportId
    except ValueError:
        # if value was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    if(airportId==tempAirportId) :
	sumTime=sumTime+delayTime
        countInst+=1
	if(delayTime>=maxTime):
		maxTime=delayTime
	if(delayTime<=minTime):
		minTime=delayTime
    else:
        if(airportId!=""):
            # write result to STDOUT
            print("For airportId: "+str(airportId)+" The minimum delay: "+str(minTime))
	    print("For airportId: "+str(airportId)+" The maximum delay: "+str(maxTime))
	    if(countInst>0):
	    	avgTime=sumTime/countInst
	    print("For airportId: "+str(airportId)+" The Average detaly: "+str(avgTime))
        minTime=-0.0
	maxTime=-0.0
	sumTime=0.0
	countInst=0
	#resetig values for further computation
	airportId=tempAirportId
	sumTime=sumTime+delayTime
        countInst+=1
	if(delayTime>=maxTime):
		maxTime=delayTime
	if(delayTime<=minTime):
		minTime=delayTime


# do not forget to output the last word if needed!
if (airportId==tempAirportId):
    # write result to STDOUT
    print("For airportId: "+str(airportId)+" The minimum delay: "+str(minTime))
    print("For airportId: "+str(airportId)+" The maximum delay: "+str(maxTime))
    if(countInst>0):
    	avgTime=sumTime/countInst
    print("For airportId: "+str(airportId)+" The Average detaly: "+str(avgTime))
