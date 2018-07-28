#!/usr/bin/env python


import sys
from operator import itemgetter

movId=0
tmpId=0
movTittle=""
rating=0.0
sumRating=0.0
countInst=0
avgRate=0.0
topMovId=0
topMovAvg=0.0
topMovTittle=""
sumRateMov={}
tittleMov={}
avgMov={}


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    dataRcv= line.split("=")
    if(int(dataRcv[3])==2): # this 3rd type differentiate where data comes from , which file
	tittleMov[dataRcv[0]]=[dataRcv[1],dataRcv[2]] # here 2nd is gener category of movie
    	
    else:
	try:
		tmpId=dataRcv[0]
		rating=float(dataRcv[1])
		if (movId==0):
			movId=tmpId
    	except ValueError:
		# ignore/discard this line
		continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    	if(tmpId in sumRateMov):
		sumRateMov[tmpId][0]+=rating
		sumRateMov[tmpId][1]+=1
    	else:
		sumRateMov[tmpId]=[rating,1]
	

for x in sumRateMov:
	avgMov[x]= sumRateMov[x][0]/sumRateMov[x][1]

sortedDict=sorted(avgMov.items(), key=itemgetter(1))
topM=max(sortedDict,key=itemgetter(1))

topMovTittle=tittleMov[topM[0]]

print("Movie with top average rating genre: "+str(topMovTittle[1]))
