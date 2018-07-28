# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 20:10:58 2017

@author: JUNAID
"""


from __future__ import print_function

import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.cross_validation import train_test_split
# Parameters
learning_rate = 0.02
n_epochs = 150
batch_size = 5
display_step = 1
# import iris dataset
iris = datasets.load_iris()
data_x = iris.data 
data_y = iris.target
classes=3
features=4
sizeY=len(data_y)
dataYClasses=np.zeros((sizeY,classes),dtype=int)
for x in range(sizeY):
    dataYClasses[x][data_y[x]]=1
    #print(dataYClasses[x])
    
train_data_x, test_data_x, train_data_y, test_data_y = train_test_split(data_x, dataYClasses, test_size=0.10, random_state=10)

sizeTrain=len(train_data_y)
sizeTest=len(test_data_y)
X = tf.placeholder(tf.float32, [None, features])
Y = tf.placeholder(tf.float32, [None,classes])

w = tf.Variable(tf.random_normal(shape=[features,classes],mean=0.0, stddev=0.01), name="weights")
b = tf.Variable(tf.zeros([1,classes]), name="bias")
tensor_flow_logs='E:\\tensorflow_logs'

with tf.name_scope('Model'):
    logitsTf = tf.matmul(X, w) + b
    pred = tf.nn.softmax(logitsTf) # Softmax
# Tensorboard's Graph visualization more convenient
    entropy = tf.nn.softmax_cross_entropy_with_logits(labels=Y,logits=logitsTf)
with tf.name_scope('Loss'):  # Minimize error using cross entropy
    loss = tf.reduce_mean(entropy) 
    # Create a summary to monitor cost tensor
    cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(pred), reduction_indices=1))
     
with tf.name_scope('SGD'):
# Gradient Descent
    optimizer =tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(entropy)
with tf.name_scope('Accuracy'):
    # Accuracy
    acc = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
    acc = tf.reduce_mean(tf.cast(acc, tf.float32))


# Initializing the variables
init = tf.global_variables_initializer()

# Create a summary to monitor accuracy tensor
tf.summary.scalar("accuracyQ1", acc)
# Create a summary to monitor accuracy tensor
# Merge all summaries into a single op
tf.summary.scalar("lossQ1", loss)

tf.summary.histogram("Histogram_MeanQ1", cost)

merged_summary_op = tf.summary.merge_all()


with tf.Session() as sess:
    sess.run(init)
    # op to write logs to Tensorboard
    summary_writer = tf.summary.FileWriter(tensor_flow_logs, graph=tf.get_default_graph())
    n_batches = int(len(train_data_x)/batch_size)
    for i in range(n_epochs): # train the model n_epochs times
        #print("Epoch #: "+str(i))
        averageCost=0.0
        avgAccuracy=0.0
        for j in range(n_batches):
            X_batch = train_data_x[j*batch_size:(j+1)*batch_size]
            Y_batch = train_data_y[j*batch_size:(j+1)*batch_size]
            
            trainBatch={X: X_batch, Y:Y_batch}
            _, c, summary=sess.run([optimizer, loss,merged_summary_op], feed_dict=trainBatch)
            
            averageCost+=c/batch_size
            singCost=cost.eval(trainBatch)
            accuracySingle=acc.eval(trainBatch)
            avgAccuracy+=accuracySingle
            summary_writer.add_summary(summary, i * n_batches + j)
            
            #if(j%1==0):
        averageCost=averageCost/n_batches
        avgAccuracy=avgAccuracy/n_batches
        print("Loss & Accuracy is epoc #: "+str(i)+" is : "+str(averageCost)+" : "+str(accuracySingle))
                
                
    n_batches_test = int(len(test_data_x)/batch_size)
    total_correct_preds = 0.0
    print("number of block in test: "+str(n_batches_test))
    accuracyTest=0.0
    lossTest=0.0
   
    testBatch={X: test_data_x, Y:test_data_y}
    _, loss_batch, logits_batch = sess.run([optimizer, loss, logitsTf],feed_dict=testBatch)
    
    testLoss=loss_batch/len(test_data_y)
    testAccuracy=acc.eval(testBatch)
    
    print("Loss on test set data is:  {0}".format(testLoss))
    print("Accuracy on test set data is:  {0}".format(testAccuracy))
        
 



