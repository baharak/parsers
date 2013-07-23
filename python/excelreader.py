# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 22:08:06 2013

@author: bsaberid
"""

import sys
import csv

with open(sys.argv[1], 'rb') as csvreading:
    
    reader = csv.reader(csvreading,  delimiter=',', quoting=csv.QUOTE_ALL)
    counter = 0
    for row in reader:
        if reader.line_num > 26:
            row = [col.replace(' /// ',',').replace('---','') for col in row]
            selectedcols = [row[0],row[14],row[23] , row[18],row[17],row[10],row[7]]
            print '\t'.join(selectedcols)
            
             
        
    
 


