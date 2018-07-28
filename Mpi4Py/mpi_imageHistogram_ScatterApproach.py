# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:45:47 2017

@author: JUNS
"""

from mpi4py import MPI
import numpy as np
import cv2
import matplotlib.pyplot as plt


def histoGramOfFreqInAnyImage(comm,size,rank,root,data,imageType):
   
    
    
   
     ##################for greyScale image ##############
    if(imageType==1):
        imgGrey=data
        arOfFrequenciesGrey=np.zeros(256,int)
        # in loop below I divide rows by adding jump in loop triverse, so each process access different rows according to rank
        for i in range(rank,len(imgGrey)):
            for j in range(len(imgGrey[i])):
                arOfFrequenciesGrey[imgGrey[i][j]]+=1
                               
        return arOfFrequenciesGrey
##################for RGB image ##############
    if(imageType==2):
        imgRGB=data
        arOfFrequenciesRGB=np.zeros([256,3],int)#3 rows for different layer frequencies
   # I receive data by scatter so data is already divided
        for i in range(rank,len(imgRGB)):
            for j in range(len(imgRGB[i])):
                #in below line I go to respective index of my local frequency array and increment gainst value
                firstlayer=0
                secondLayer=1
                thirdLayer=2
                arOfFrequenciesRGB[imgRGB[i][j][firstlayer]][firstlayer]+=1
                arOfFrequenciesRGB[imgRGB[i][j][secondLayer]][secondLayer]+=1
                arOfFrequenciesRGB[imgRGB[i][j][thirdLayer]][thirdLayer]+=1
                               
        return arOfFrequenciesRGB
    
def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    root = 0
    imageName='city.jpg'
        ##############below line image type=1 for grayScale 
    imageType=1
    if(imageType==1):
        startTime=MPI.Wtime()
        arOfFrequenciesGrey=np.zeros(256,int)
        if(rank==root):
            imgGrey = cv2.imread(imageName,cv2.IMREAD_GRAYSCALE)
            dataToScatter=np.vsplit(imgGrey,size)
        else:
            dataToScatter=None
        recvdata=comm.scatter(dataToScatter,root=root)
        arOfFrequenciesGrey=histoGramOfFreqInAnyImage(comm,size,rank,root,recvdata,imageType)
        resultantArOfFrequencies=np.zeros(256,int)
        oprt = MPI.SUM
        comm.Reduce(arOfFrequenciesGrey,resultantArOfFrequencies,root=root,op=oprt)
        comm.Barrier()
        if(rank==root):
            #print("The final frequencies from 0-255 calculated by all processes are:")
            print("total number of pixels GreyScale: "+str(sum(resultantArOfFrequencies)))
            print("Total burn Time GreyScale: "+str(MPI.Wtime()-startTime))
        
            indexesOdValues=np.arange(0,256)
            #***in case of grey scale all 3 dimention values are same so all three line plot at same place
            plt.plot(indexesOdValues,resultantArOfFrequencies,label="Graph for GreyScale",color='k')
            plt.ylabel('Value from 0 -- 256')
            plt.xlabel('Frequncies against each value')
            plt.legend()
            plt.show()
    ##############below line imageType=2 for RGB
    imageType=2
    if(imageType==2):
        startTime=MPI.Wtime()
        arOfFrequencies=np.zeros([256,3],int)
        if(rank==root):
            imgRGB = cv2.imread(imageName)
            dataToScatter=np.vsplit(imgRGB,size)
        else:
            dataToScatter=None
        recvdata=comm.scatter(dataToScatter,root=root)
        arOfFrequencies=histoGramOfFreqInAnyImage(comm,size,rank,root,recvdata,imageType)
        resultantArOfFrequencies=np.zeros([256,3],int)
        oprt = MPI.SUM
        comm.Reduce(arOfFrequencies,resultantArOfFrequencies,root=root,op=oprt)
        comm.Barrier()
        if(rank==root):
            #print("The final frequencies from 0-255 calculated by all processes are:")
            print("total number of pixels RGB (each pixel has 3 values): "+str(sum(resultantArOfFrequencies[:,0])))
            print("Total burn Time RGB: "+str(MPI.Wtime()-startTime))
        
            indexesOdValues=np.arange(0,256)
            #***in case of grey scale all 3 dimention values are same so all three line plot at same place
            plt.plot(indexesOdValues,resultantArOfFrequencies[:,0],label="Graph for 1st dimention colour",color='r')
            plt.plot(indexesOdValues,resultantArOfFrequencies[:,1],label="Graph for 2nd dimention colour",color='g')
            plt.plot(indexesOdValues,resultantArOfFrequencies[:,2],label="Graph for 3rd dimention colour",color='b')
            plt.ylabel('Value from 0 -- 256')
            plt.xlabel('Frequncies against each value')
            plt.legend()
            plt.show()
            
    

# run the main function
main()


