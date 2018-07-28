#!/usr/bin/env python


#from nltk.corpus import stopwords 
import re # this is regular expression library to recognize if data match some category
#import string
import sys

#
#punctuation=string.punctuation
#digits="0123456789"
#stopWords = set(stopwords.words('english'))
stopWords=[u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now', u'd', u'll', u'm', u'o', u're', u've', u'y', u'ain', u'aren', u'couldn', u'didn', u'doesn', u'hadn', u'hasn', u'haven', u'isn', u'ma', u'mightn', u'mustn', u'needn', u'shan', u'shouldn', u'wasn', u'weren', u'won', u'wouldn']


def removeStopWords(inputLine):
    tokenizeLine=inputLine.split(" ")
    cleanedList=list()
    cleanedLine=' ' # I assigng space intentionaly to join list in space as well
    for w in tokenizeLine:
        if((w.lower() not in stopWords and w not in " ")):
          cleanedList.append(w)  
    cleanedLine=cleanedLine.join(cleanedList)
    return cleanedLine
def removePuncNumber(line):
    cleanedLine=re.sub(r"[^A-Za-z]",' ',line)
    return cleanedLine

for inLine in sys.stdin:        
    inLine=removePuncNumber(inLine)#after this line will clean from punctuation and number digits
    inLine=removeStopWords(inLine)
    inLine=inLine.strip()
    if((not inLine.isspace()) and inLine!=''):
    	print(inLine)
