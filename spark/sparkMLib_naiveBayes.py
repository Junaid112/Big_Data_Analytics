#!/usr/bin/env python

from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.ml.feature import IDF


spark = SparkSession \
    .builder \
    .appName("e8_3") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc=spark.sparkContext
sqlContext = SQLContext(sc)

spamFile=sc.textFile("Spam.csv")
fileLineTokens=spamFile.map(lambda line:(line.split(",",1)[0],line.split(",",1)[1]))
fileDf=sqlContext.createDataFrame(fileLineTokens, ["categ", "text"])

training_data, testing_data = fileDf.randomSplit([0.8, 0.2])

categoryIndexerUnit = StringIndexer(inputCol="categ", outputCol="label")
tokenizerUnit = Tokenizer(inputCol="text", outputCol="words")
tokenizedWords=tokenizerUnit.transform(fileDf)
stoRemover = StopWordsRemover(inputCol="words", outputCol="clean_content")
tweetWordsData=stoRemover.transform(tokenizedWords)
hashingTermFrequecies = HashingTF(inputCol="clean_content", outputCol="rawFeatures", numFeatures=500)
featuredData = hashingTermFrequecies.transform(tweetWordsData)
idfData = IDF(inputCol="rawFeatures", outputCol="features")
naiveBaysClassifier = NaiveBayes(smoothing=1.0, modelType="multinomial")

# here I didn't use idf model because there is only one main doc and through hashing tf naive bays can idetify between sapm or not
pipeline = Pipeline(stages=[categoryIndexerUnit, tokenizerUnit,stoRemover, hashingTermFrequecies,idfData, naiveBaysClassifier])

model = pipeline.fit(training_data)
prediciton = model.transform(testing_data)

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
f1MetricScore = evaluator.evaluate(prediciton)
print("F1 metric score is: ")
print(f1MetricScore)