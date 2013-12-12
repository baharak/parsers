# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 19:09:24 2013

@author: bsaberid
"""

#!/bin/python

import sys
import math
import os


from collections import namedtuple
from collections import defaultdict

Atom = namedtuple('CA_pos', ['num', 'name','x','y','z'])


def run(pdb,pdbfile,d):
    def dis(a1,a2):
        return  math.sqrt(abs((a1.x-a2.x)**2+(a1.y-a2.y)**2+(a1.z-a2.z)**2))

    def fun(filename, get_neighbors):
        try:
            os.makedirs('../dist')
        except OSError:
            pass
        graph = open(filename,'w')

        pairs = set()
        degree = defaultdict(int)
        adj = defaultdict(list)
        for a1 in atoms:
             s = sorted(atoms, key = lambda a2 : dis(a1,a2) )
             s.remove(a1)
             for a2 in get_neighbors(a1, s):
                 p = ( a1,a2 )
                 if p in pairs:
                     continue
                 pairs.add((a2,a1))
                 degree[a1] += 1
                 degree[a2] += 1
                 adj[a1].append(a2)
                 adj[a2].append(a1)
                 print >> graph, a1.num+a1.name,'\t', a2.num+a2.name ,'\t', dis(a1,a2)

        return adj, degree

    def k_nearest():
        def get_neighbors2(a1, s):
            return s[:k]
        for k in range(3,len(atoms),1):
            fun('../output/knearest/graph%03d' % k, get_neighbors2)

    def fixed_dis(d):
        def get_neighbors3(a1, s):
            return filter(lambda a2: dis(a1, a2) <= d, s)
        return fun('output/degree/graph-fixed-%f' % d, get_neighbors3)

    def is_connected(adj):
        vis = set()
        u0 = atoms[0]
        s = [u0]
        while len(s):
            u = s.pop()
            if u in vis:
                continue
            vis.add(u)
            for v in adj[u]:
                if v not in vis:
                    s.append(v)
        return len(vis) == len(atoms)

    try:
        input = open(pdb , 'r')
    except IOError:
        return False

    atoms = []
    for line in input:
        line = line.strip()
        if len(line) == 0:
            continue
        word = line.split()
        #print word[0]
        if (word[0] == 'ATOM'):
            col = line.split()
            #print len(col)
            if (col[2] == 'CA'):
                a = Atom(num = col[1] , name=col[3], x=float(col[6]), y = float(col[7]) , z = float(col[8]) )
                atoms.append(a)

    adj, degree = fixed_dis(d)

    if is_connected(adj) :
      print pdbfile, " is connected"
      print >> congraph, pdbfile , '\t', len(atoms) ,'\t' ,sum(degree.values())/len(atoms) , '\t' , max(degree.values())
      if max(degree.values()) <= 7:
         print >> maxDegre7, pdbfile , '\t' , len(atoms) ,'\t' ,sum(degree.values())/len(atoms) , '\t' , max(degree.values())
      return True
    return False



if __name__ == '__main__':
    try :
        input_list = open(sys.argv[1],'r') # it will be protein list
    except:
        print "can not open the list of proteins"

    d = int(sys.argv[2]) # cutoff distance
    selectedlist = 'finallist-%f'%d
    erfile = 'errorFile-%f'%d
    degreefile = 'maxdegree7'
    congraph  = open(selectedlist,'w')
    maxDegre7 = open(degreefile, 'w')
    errorfile = open(erfile,'w')
    counter = 0

    for pdbfile in input_list:
        print pdbfile

        pdbfile = pdbfile.strip()
        pdbfile = pdbfile.upper()

        #pdb = '../../testdata/sampledir/' + pdbfile + '.pdb'
        pdb = '../testdata/pdbsss/' + pdbfile + '.pdb'
        print pdb

        try:
            counter += run(pdb , pdbfile ,d)
        except:
            print >> errorfile, pdbfile

    print 'Number of the pdbs with d = %f is %d'% (d, counter)
