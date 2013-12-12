#!/bin/python

import sys
import math
import os
from collections import defaultdict

def getIndex(pdbfile, assign_file, output_file):
   index = 0;
   cAdict = defaultdict()
   lines = []
   atomsBegin = False
   done = False
   for line in open(pdbfile,'r'):
      line = line.strip()
      if len(line) == 0:
         continue
      word = line.split()
      if (word[0] == 'ATOM'):
         atomsBegin = True
         col = line.split()
         if (col[2] == 'CA'):
            cAdict[index] = line
            index = index + 1
      else:
         if atomsBegin and not done:
            for line2 in open(assign_file, 'r'):
               id = line2.strip()
               print >> output_file, cAdict.get(int(id))
            done = True
         print >> output_file , line


if __name__ == '__main__':

   # input_list = open(sys.argv[1],'r') # it will be the first col
   pdbfile = sys.argv[1]
   # for pdbfile in input_list:
   pdbfile = pdbfile.strip()
   pdbfile = pdbfile.upper()
   pdb = '/home/bsaberid/Dropbox/research/pdb/testdata/pdbsss/'+ pdbfile + '.pdb'
   print pdb
   out_file = 'myOutput/'+ pdbfile + '-mine' + '.pdb'
   with open(out_file, 'w') as output_file:
           getIndex(pdb, sys.argv[2], output_file)







