#!/bin/python

import copy
import os
import sys
import json
import math
import random
import re
import csv

from collections import namedtuple
from collections import defaultdict


if __name__ == '__main__':

    dirname = 'output'

    try:
        os.makedirs(dirname)
    except OSError:
        if os.path.exists(dirname):
        # We are nearly safe
            pass
        else:
            # There was an error on creation, so make sure we know about it
            raise

    input_file = sys.argv[1]
    block_name = set(sys.argv[2].split(','))
    output_name =  os.path.basename(input_file) + '-' + sys.argv[2].replace(' ', '_')
    output_name = os.path.join(dirname,output_name)
    print output_name

    data = defaultdict(list);
    f = open(input_file, 'r')
    flag = name =  None
    enslist = {}
    emptyline = 0
    for line in f:

        line = line.strip()
        if not line : # seperate blocks by two consecutive empty lines
            emptyline +=1
        else:
            emptyline = 0
        word = line.split('\t')
        pvals = []
        if flag:
            try:
                pvals = line.split(';')
                _,_,rawp = pvals[4].partition('=')
                _,_,adjp = pvals[5].partition('=')
                data [flag] += [rawp, adjp]
            except:
                raise

        flag = None
        if (word[0] in block_name): # start of the block we care
            name = word[2]
            data[name] += [word[1]]
            enslist[name] = []
            flag = name;

        elif emptyline == 2: # end of the block
            name = None

        if(name and word[0].startswith('ENS')):
            enslist[name].append(word[5])

#    for index, value in data.iteritems():
#        enses = ','.join(set(enslist[index]))
#        print index, '\t'.join(value + [enses])
#        print index , len(set(enslist[index]))

    with open(output_name,'wb') as csvwriting:
        writer = csv.writer(csvwriting, delimiter = '\t',quoting=csv.QUOTE_MINIMAL)
        header = ["ID", "Block_Name", "rawP", "adjP", "Gene List"]
        writer.writerow(header)
        for index, value in data.items():
            enses_string = ','.join(set(enslist[index]))
            print [index] + value + [enses_string]
            writer.writerow( [index] + value + [enses_string])









