"""
Created on Thu Jul 18 18:37:33 2013
@author: bsaberid
"""
import sys
import math
import os
from collections import defaultdict

if __name__ == '__main__':
 
    probIds = open(sys.argv[1],'r') # it will be the first col
    biomartfile = open(sys.argv[2],'r') 
    output = open('Id2Ens.txt','w')  
    hashtable = defaultdict()
                       
    for line in biomartfile:
        line = line.strip()
        if len(line) == 0:
            continue
        word = line.split()
        if 1 < len(word) < 3:
            hashtable[word[1]] = word[0]
            
    print >> output,'AffyId','\t','EnsembleId' 
    for line in probIds:
        line = line.strip()
        if len(line) == 0:
            continue  
        if hashtable.get(line,None):
            print >>  output ,line,'\t', hashtable.get(line,None)

  
      