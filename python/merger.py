"""
Created on Fri Jul 19 13:55:43 2013

@author: bsaberid
"""

import sys
from collections import defaultdict

if __name__ == '__main__':
    
    hashtable = defaultdict()
    output = open('U33.txt','w') 
    
    num_long  = sum(1 for line in open(sys.argv[1],'r')) 
    num_short = sum(1 for line in open(sys.argv[2],'r')) 
    print 'longer then shorter : ', num_long, num_short
    
    for line in open(sys.argv[1],'r'): 
        line = line.strip()
        if len(line) == 0:
            continue
        word = line.split('\t')
        word += ['']*(5 - len(word))
        hashtable[word[0]] = word[1:]
    
    counter = 0
    for line in open(sys.argv[2],'r'):
        line = line.strip()
        if len(line) == 0:
            continue   
        word = line.split('\t')
        word += ['']*(4 - len(word))
        if word[0] in hashtable:
            words_combined = [word[0]] + hashtable[word[0]] + [word[2]]+ [word[3]]
            print >> output, '\t'.join(words_combined)
        else:
            counter = counter + 1
    print "Check the uniquness"
       

