#!/usr/bin/env python

from __future__ import print_function

from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import UserDefinedFunction


#import matplotlib.pyplot as plt

spark = SparkSession \
    .builder \
    .appName("e7") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc=spark.sparkContext
sqlContext = SQLContext(sc)

dfIris = sqlContext.read.load('iris.csv',format='com.databricks.spark.csv',header='true',inferSchema='true')

mapLabels = {'setosa': 1, 'versicolor':2 , 'virginica':3}

toNumber = UserDefinedFunction(lambda x: mapLabels[x], IntegerType())


dfIris2 = dfIris.withColumn('Species',toNumber(dfIris['Species']))

def labeledData(dfData):
    # here we pich the feature data along with label
    return dfData.rdd.map(lambda row: LabeledPoint(row[-1], row[:-1]))

labelData=labeledData(dfIris2)
# usually we divide in 80/20 % data for train and text
train_data, test_data = labelData.randomSplit([0.8, 0.2])

model = DecisionTree.trainClassifier(train_data, numClasses=4, maxDepth=3,categoricalFeaturesInfo={},impurity='gini', maxBins=32)

print(model.toDebugString())

from pyspark.mllib.evaluation import MulticlassMetrics

def predicitonLabels(model, test_data):
    predictionsResult = model.predict(test_data.map(lambda r: r.features))
    return predictionsResult.zip(test_data.map(lambda r: r.label))

# in below funciton output the measurements like precision(accuraccy) and F1 score
def printMeasurementMetrics(predictions_and_labels):
    metrics = MulticlassMetrics(predictions_and_labels)
    print('Precision Result of setosa: ', metrics.precision(1))
    print('Precision Result of versicolor:', metrics.precision(2))
    print('Precision Result of virginica:', metrics.precision(3))
    print ('F-1 Score:         ', metrics.fMeasure())
    print ('Confusion Matrix\n', metrics.confusionMatrix().toArray())

predictionWithLabels = predicitonLabels(model, test_data)

printMeasurementMetrics(predictionWithLabels)
