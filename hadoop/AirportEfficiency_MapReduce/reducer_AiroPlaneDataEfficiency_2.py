#!/usr/bin/env python

#from operator import itemgetter
import sys
from operator import itemgetter

airportId=""
tempAirportId=""

delayTime=0.0
sumTime=0.0
countInst=0
aTimeList=list()
nMinimumDelay=10 # top 10 minimum delays to compute rank of airports

#below function maintaim list of sorted minimum delays time to make rank list
#which Airport has minimum delays average, rank 1st and so on for other's
def adjustElement(lst,elm,aName,nMinimumDelay):
	sz=len(lst)
	
	for i in range(sz):
		if(elm<=lst[i][1] and i==0):
			lst.insert(i,[aName,elm])
			break
		if(elm<=lst[i][1] and i==sz-1):
			lst.insert(i,[aName,elm])
			break
		if(i>0 and i<sz-1 and elm>=lst[i][1] and elm<=lst[i+1][1]):
			lst.insert(i+1,[aName,elm])
			break
	
	#if(len(lst)>nMinimumDelay):
		#lst=lst[:10]
	sortList=sorted(lst, key=itemgetter(1))
	top10=sortList[:nMinimumDelay]	
	return top10

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    airportIdstr, delayTimestr = line.split("\t",1)

    try:
        tempAirportId = airportIdstr
	delayTime=float(delayTimestr)
	if (airportId==""):
		airportId=tempAirportId
    except ValueError:
        # delayTimestr was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if(airportId==tempAirportId):
	sumTime=sumTime+delayTime
        countInst+=1
    else:
        if(airportId!=""):
            # write result to STDOUT
	    if(countInst>0):
	    	avgTime=sumTime/countInst
		sizeList=len(aTimeList)
		if (len(aTimeList)>0):	    	
			aTimeList=adjustElement(aTimeList,avgTime,airportId,nMinimumDelay)
		else:
			aTimeList.append([airportId,avgTime])
	sumTime=0.0
	countInst=0
	airportId=tempAirportId
	sumTime=sumTime+delayTime
        countInst+=1

#output the last different line!
if (airportId==tempAirportId):
    # write result to STDOUT for remaining if single one different
    if(countInst>0):
    	avgTime=sumTime/countInst
	aTimeList=adjustElement(aTimeList,avgTime,airportId,nMinimumDelay)
for x in range(len(aTimeList)):
	#because at [x][0] is my airport name and [x][1] is my delay
    print("Airport: "+str(aTimeList[x][0])+" has Rank: "+str(x+1)+" with Average Arrival detaly: "+str(aTimeList[x][1]))
