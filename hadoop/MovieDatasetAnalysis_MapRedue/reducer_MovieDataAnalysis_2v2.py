#!/usr/bin/env python


import sys
from operator import itemgetter

sumRateMov={}
tittleMov={}
avgMov={}
userId=0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    	line = line.strip()
    	dataRcv= line.split("=")
    	
	   
	try:
		tmpId=int(dataRcv[0])# this is user ID
		rating=float(dataRcv[1])
		if (userId==0):
			userId=tmpId
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
	if(sumRateMov[x][1]>40):#only those user who have more than 40 time tatings
		avgMov[x]= sumRateMov[x][0]/sumRateMov[x][1]

sortedDict=sorted(avgMov.items(), key=itemgetter(1))
lowM=min(sortedDict,key=itemgetter(1))

print("User with who rate low: "+str(lowM[0])+" Average_Rating: "+str(lowM[1]))
