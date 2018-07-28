#!/usr/bin/env python


import sys
import math


totalNumOfFiles=5 # we an change logic for more than 5 files
#fr means frequency here, 
wordDictionary={}
wordCountPerFile=[0,0,0,0,0]

#below function will check nmber of nor zeros element in aray to know that how many files contain a perticualr word
def countNonZeroInAray(ar):
	countNZ=0
	for i in range(len(ar)):
		if(ar[i]!=0):
			countNZ+=1
	return countNZ


def main():
	fileIdx=0
# I know the input from mapper is sorted so I imlement logic accordingly
	for dataLine in sys.stdin:
		dataAray=dataLine.split('\t')
		if(dataAray[0] not in wordDictionary):
			wordDictionary[dataAray[0]]={"TFIDF":[0.0,0.0,0.0,0.0,0.0],"overAllTFIDF":0.0,"IDF":0.0,"TF":[0,0,0,0,0],"frPerFile":[0,0,0,0,0]}
		
		#now I know word is added in dictionary
		try:
			fileIdx=int(dataAray[1])-1
			wordDictionary[dataAray[0]]["frPerFile"][fileIdx]+=1
			wordCountPerFile[fileIdx]+=1
		except ValueError:
	        # if value was not a number, so silently
        	# ignore/discard this line
        		continue
		
	for word in wordDictionary:
		if(wordCountPerFile[0]!=0):
			wordDictionary[word]["TF"][0]=float(wordDictionary[word]["frPerFile"][0])/float(wordCountPerFile[0])# for file number 1
		if(wordCountPerFile[1]!=0):
			wordDictionary[word]["TF"][1]=float(wordDictionary[word]["frPerFile"][1])/float(wordCountPerFile[1])# for file number 2
		if(wordCountPerFile[2]!=0):
			wordDictionary[word]["TF"][2]=float(wordDictionary[word]["frPerFile"][2])/float(wordCountPerFile[2])# for file number 3
		if(wordCountPerFile[3]!=0):
			wordDictionary[word]["TF"][3]=float(wordDictionary[word]["frPerFile"][3])/float(wordCountPerFile[3])# for file number 4
		if(wordCountPerFile[4]!=0):
			wordDictionary[word]["TF"][4]=float(wordDictionary[word]["frPerFile"][4])/float(wordCountPerFile[4])# for file number 5
		wordDictionary[word]["IDF"]=float(countNonZeroInAray(wordDictionary[word]["frPerFile"]))/float(totalNumOfFiles)
		#wordDictionary[word]["IDF"]=math.log(wordDictionary[word]["IDF"])
		wordDictionary[word]["TFIDF"][0]=wordDictionary[word]["TF"][0]*wordDictionary[word]["IDF"]
		wordDictionary[word]["TFIDF"][1]=wordDictionary[word]["TF"][1]*wordDictionary[word]["IDF"]
		wordDictionary[word]["TFIDF"][2]=wordDictionary[word]["TF"][2]*wordDictionary[word]["IDF"]
		wordDictionary[word]["TFIDF"][3]=wordDictionary[word]["TF"][3]*wordDictionary[word]["IDF"]
		wordDictionary[word]["TFIDF"][4]=wordDictionary[word]["TF"][4]*wordDictionary[word]["IDF"]	
		wordDictionary[word]["overAllTFIDF"]=float(sum(wordDictionary[word]["frPerFile"]))/float(sum(wordCountPerFile))
		print("%s\t%s\t TotalWords_EachFile: %s"%(word,wordDictionary[word],wordCountPerFile))
main()
