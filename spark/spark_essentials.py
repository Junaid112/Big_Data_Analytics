#!/usr/bin/env python

#Author : JUNAID AHMED GHAURI
from pyspark.sql import SparkSession
from pyspark import SparkContext
import sys
import re

sc=SparkContext()

spark = SparkSession \
    .builder \
    .appName("bda_exercise") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
# below is the function to remove punctuation so I can find spark word wihtin line as well even join with punctuations
def cleanLine(line): 
    cleanedLine=re.sub(r"[^A-Za-z]",' ',line)
    return cleanedLine

file1=sc.textFile("README.md")
file2=sc.textFile("CHANGES.md")

#cleanLine will remove punctuations so I can split word by space properly
file1Words=file1.flatMap(lambda line: cleanLine(line).split(" "))
print(file1Words.collect())
# check for both spark with small and caps as well
file1WordsFiltered=file1Words.filter(lambda x: x.lower()=='spark')
file1WordsFilteredMap=file1WordsFiltered.map(lambda word: (word.lower(), 1))
print(file1WordsFilteredMap.collect())
# my reduce will only count spark occurance because I already filtered
resultFile1=file1WordsFilteredMap.reduceByKey(lambda a, b: a + b)         
print(resultFile1.collect())

#cleanLine will remove punctuations so I can split word by space properly
file2Words=file2.flatMap(lambda line: cleanLine(line).split(" "))
print(file2Words.collect())
# check for both spark with small and caps as well
file2WordsFiltered=file2Words.filter(lambda x: x.lower()=='spark')
file2WordsFilteredMap=file2WordsFiltered.map(lambda word: (word.lower(), 1))
print(file2WordsFilteredMap.collect())
# my reduce will only count spark occurance because I already filtered
resultFile2=file2WordsFilteredMap.reduceByKey(lambda a, b: a + b)
print(resultFile2.collect())

# i combine the both result rom different files
finalresult=resultFile1+resultFile2
# now I know that I have same key from both file so I reduce to get final result
finalresult=finalresult.reduceByKey(lambda a, b: a + b)
print(finalresult.collect())             


