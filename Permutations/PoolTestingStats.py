#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
*********************************************
* Evaluate testing results based on pools
* version: 20220105
* By: NF <feranick@hotmail.com>
***********************************************
'''
print(__doc__)

import numpy as np
import sys, os.path, h5py, csv
import matplotlib.pyplot as plt

def main():
    # Parameter definition
    numStud = 3500
    preval = 0.06
    numPools = 350
    iterations = 100
    
    print(" # Students:", numStud)
    print(" Prevalence:", preval*100,"%")
    print(" # Pools:", numPools)
    print(" Permutations:", iterations)
    
    arrayPosPools = np.zeros(iterations)
     
    # main array with student testing data
    popStud = np.random.choice([0, 1], size=(numStud,), p=[1-preval, preval])
    
    #unique, counts = np.unique(popStud, return_counts=True)
    #print(popStud)
    #print(dict(zip(unique, counts)))

    # New routine, optimized for speed
    def func(array):
        index = 0
        if np.any(array == 1):
            index+=1
        return index
    
    numMembersPos = np.zeros((iterations, 4))
    
    for i in range(iterations):
        newPopStud = np.random.permutation(popStud)
        newPools = np.stack(np.split(newPopStud, numPools), axis=0)
        arrayPosPools[i] = np.count_nonzero(np.apply_along_axis(func, axis=1, arr=newPools)==1)
        
        numPosPools = np.zeros(newPools.shape[0])
        members = np.zeros((newPools.shape[0],4))
        
        for j in range(newPools.shape[0]):
            for s in range(4):
                members[j,s] = np.count_nonzero(newPools[j,:]==s)
    
        for k in range(4):
            numMembersPos[i,k] = np.count_nonzero(members == 10-k)
        
    print("\n Average number of negative pools:",np.average(numMembersPos[:,0]))
    print(" Average number positive pools:",np.average(arrayPosPools))
    print(" Average Number of positive pools with 1 member:",np.average(numMembersPos[:,1]))
    print(" Average Number of positive pools with 2 member:",np.average(numMembersPos[:,2]))
    print(" Average Number of positive pools with 3 member:",np.average(numMembersPos[:,3]),"\n")
          
    plt.hist(numMembersPos[:,0], density=True, bins=30, label="Negative Pools")
    addLabelsPlot(plt)
    plt.show()
    
    plt.hist(arrayPosPools, density=True, bins=30, label="Positive Pools")
    addLabelsPlot(plt)
    plt.show()
    
    plt.hist(numMembersPos[:,0], density=True, bins=30, label="Negatives")
    plt.hist(arrayPosPools, density=True, bins=30, label="1+ in pool")
    plt.hist(numMembersPos[:,1], density=True, bins=30, label="2+ in pool")
    plt.hist(numMembersPos[:,2], density=True, bins=30, label="3+ in pool")
    addLabelsPlot(plt)
    plt.show()

    #plt.savefig('histogram.png', dpi = 160, format = 'png')
    
def addLabelsPlot(plt):
    plt.ylabel('Probability')
    plt.xlabel('Number of pools')
    plt.legend()

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
