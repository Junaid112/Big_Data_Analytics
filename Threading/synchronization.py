# -*- coding: utf-8 -*-
"""

@author: Junaid Ahmed Ghauri
"""

import threading
import time
import numpy as np

 


def axpyOperator(load): # part a multiply first vector with a scalor and add in to other vector
    loadInt=int(load) # change float to int
    print(loadInt)
    lock1.acquire() 
    global TNrAxpyOperator
    #tid = threading.currentThread().ident
    for i in range(TNrAxpyOperator*loadInt,(TNrAxpyOperator+1)*loadInt):
        result1[i]=alpha*v[i]+w[i]
    lock1.release()
    
    endTime=time.time()-startTime
    print("end time "+str(endTime)+"of 1st operation # "+str(TNrAxpyOperator))
    TNrAxpyOperator=TNrAxpyOperator+1

def dotProduct(load):  # part b pf the last exercise compute dot product of vectors
    
    global SumOfDotProduct
    loadInt=int(load) # change float to int
    print(loadInt)
    lock2.acquire()
    global TNrDotPrd
    #tid = threading.currentThread().ident
    for i in range(TNrDotPrd*loadInt,(TNrDotPrd+1)*loadInt):
       SumOfDotProduct+=(v[i]*w[i])
       
    lock2.release()
    endTime=time.time()-startTime
    print("end time "+str(endTime)+"of 1st operation # "+str(TNrDotPrd))
    TNrDotPrd=TNrDotPrd+1
    
def serialDotProduct():   # this function is to check whether serial approach on big vectors consume nore time than threads
    for i in range(0,N-1):
        print(i)
        result1[i]=alpha*v[i]+w[i]
    

# Main Execution starts from here

nThreadStr = input("Enter Number of threads: ")  # t o t a l number o f t h r e a d s
nThread=int(nThreadStr)

NStr= input("Enter length of the vectors: ") # length of both vectors
N=int(NStr)
threads = []
startTime=time.time()
TNrAxpyOperator=0
TNrDotPrd=0
SumOfDotProduct=0
v = np.random.randint(9, size=N) #a list of N random numbers 1-9

w = np.random.randint(9, size=N) #a list of N random numbers 1-9
result1=np.random.randint(1, size=N)  # result 1
  # result 2
alpha=2
lock1 = threading.Lock()
lock2 = threading.Lock()
for i in range(nThread):
    t=threading.Thread(target=axpyOperator,args=(N/nThread,))
    t.start()
    threads.append(t)
    t2=threading.Thread(target=dotProduct,args=(N/nThread,))
    t2.start()
    threads.append(t2)
    
for th in threads:
    th.join()
#serialDotProduct()
#endTime=time.time()-startTime
#print(endTime)






    
    
    
    



