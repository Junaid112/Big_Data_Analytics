#!/usr/bin/env python

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.types import DateType
import pandas as pd
from pyspark.sql import SQLContext
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt



spark = SparkSession \
    .builder \
    .appName("e7") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc=spark.sparkContext
sqlContext = SQLContext(sc)

def parse_date(td): # the age I calculated is in days so to convert in to desireable format this funciton works
    resYear = float(td.days)/364.0                 
    resMonth = int((resYear - int(resYear))*364/30) 
    resYear = int(resYear)
    return str(resYear) + "Years" + str(resMonth) + "Month"




#load students.json file as dataFrame 
dframe = spark.read.json("students.json")
#part 1 according to instructions
df=dframe.na.fill(dframe.select(mean('points')).collect()[0][0],["points"])
#part 2 according to instructions
df=df.na.fill("--",["last_name"])
df=df.na.fill("unknown",["dob"])
#part 3 and 4 according to instructions
dbCol = df.select('dob').collect()
dfPan=df.toPandas()


dobT = []
# convert all dates of births in desired format
for i in range(len(dbCol)):
    try:
        t = pd.to_datetime(dbCol[i][0])
        dobT.append(t.strftime('%d-%m-%Y'))
    except:
        dobT.append("unknown")
td=pd.to_datetime('today')
age=[]
# below loop is calculating age
for i in range(len(dbCol)):
    try:
        l = pd.to_datetime(dbCol[i][0])
        age.append(parse_date((td-l)))
    except:
        age.append("unknown")
#convert to dataFrame pandas
agePf=pd.DataFrame(age)
dobPf=pd.DataFrame(dobT)
#dfPan=pd.concat([dfPan,dobPf], axis=1)
dfPan.dob=dobPf
dfPan=pd.concat([dfPan,agePf], axis=1)
#dfPan.show()
dfPan=dfPan.astype(str)
dfFinal=sqlContext.createDataFrame(dfPan)
dfFinal.show()
#part 5 and 6
orgDf=df
df=dfFinal
df2=df.withColumn("points",when((df["points"]>(df.agg({"points":"stddev_pop"}).collect()[0][0]+df.agg({"points":"mean"}).collect()[0][0])),20).otherwise(df["points"]))
df2.show()
hist=df2.groupBy("points").count() # this will count histogram frequencies according to key
hist=hist
hist.show()
histList=hist.select('points','count').collect()
print(histList)

indexesOdValues=np.arange(0,25)
arOfFrequencies=np.zeros(25,int)
for x in histList:
    arOfFrequencies[int(x[0])]=int(x[1])
    

plt.plot(indexesOdValues,arOfFrequencies,label="Graph for frequencies",color='k')
plt.ylabel('Value ')
plt.xlabel('Frequncies against each value')
plt.legend()
plt.show()
#spark.stop()



