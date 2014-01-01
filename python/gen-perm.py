#!/usr/bin/python
import itertools

def f(n, k):
    cnt = 0
    c = 0
    for p in sorted(itertools.permutations(range(n), k)):
        if c == 0:
            cnt += 1
            print 'static void fill%dk%d_%04d(List<int[]> list) {' % (n, k, cnt) 
        print 'list.add(new int[]%s);' % str(p).replace('[', '{').replace(']', '}').replace('(', '{').replace(')', '}')
        c += 1
        if c == 100:
            print '}'
            c = 0
            
    if c != 100:
        print '}'
            
    print 'static int[][] getPerm%dk%d() {' % (n, k)
    print 'List<int[]> list = new ArrayList<int[]>();'
    for i in range(1, cnt + 1):
        print 'fill%dk%d_%04d(list);' % (n, k, i)
    
    print
    print 'final int k = %d;' % (k,),
    print """
    int[][] arr = new int[list.size()][k];
	  for (int i = 0; i < list.size(); ++i)
		  for (int j = 0; j < k; ++j)
			  arr[i][j] = list.get(i)[j];
	  return arr;
  }
  
"""
    #print '%s%s' % (p, ',' if k < n else '')

if __name__ == '__main__':
    n = 7
    for k in range(1, n + 1):
        f(n, k)
        
