"""
Created on Fri Jul 19 13:55:43 2013

@author: bsaberid
"""

import sys

def group_by_key(key_columns, rows):
    """
    Argumens:
        - key_columns - e.g. 'F' or ('E', 'F')
        - rows - each row is a dictionary, e.g. {'F': 'foo', 'E': 'bla', 'G': 'bar', 'H': 'h'}
    """
    d = {}
    for row in rows:
        key = tuple([row[key_column] for key_column in key_columns])
        if key not in d:
            value = {}
            for column in row:
                if column not in key_columns:
                    value[column] = set([row[column]])
            d[key] = value
        else:
            value = d[key]
            for column in row:
                if column not in key_columns:
                    bucket = value[column]
                    bucket.add(row[column])
                    
    return d
    
def aggregate(d):
    d_aggregated = {}
    for key in d:
        buckets = d[key]
        aggregated = {}
        for column, values in buckets.iteritems():
            if '' in values:
                values.remove('')
                
            if len(values) == 0:
                aggregated[column] = ''
            elif len(values) == 1:
                aggregated[column] = list(values)[0]
            else:
                aggregated[column] = ','.join(sorted(values))

        d_aggregated[key] = aggregated
    return d_aggregated

def print_rows(file, rows, columns):
    """
    Example:
    rows = [{'E': 'e1', 'F': 'f', 'W': 'w', 'Z': 'z'}]
    print_rows('file.txt', rows, ['F', 'W', 'Z', 'Y'])
    > f <tab> w <tab> z
    """
    
    for row in rows:
        values = []
        for column in columns:
            value = row.get(column, '')
            if value is None:
                value = '(conflict)'
            values.append(value)  # row[column] if column in row else ''
        print >> file, '\t'.join(values)


def to_rows(d, key_columns):
    """
    to_rows([('e1', 'f1'): {'W': 'w', 'Z': 'z'}], ['E', 'F'])
    > [{'E': 'e1', 'F': 'f', 'W': 'w', 'Z': 'z'}]
    """
    
    for key_values, partial_row  in d.iteritems():
        partial_row = dict(partial_row)
        # parital_row == {'W': 'w', 'Z': 'z'}
        # key_values == ('e1', 'f1')
        # key_columns == ['E', 'F']
        for key_column, key_value in zip(key_columns, key_values):
            partial_row[key_column] = key_value
        yield partial_row


def join(outer_rows, inner_rows, join_columns):
    def get_join_column_values(row):
        return tuple([row[join_column] for join_column in join_columns])
    d = {}
    for inner_row in inner_rows:
        key = get_join_column_values(inner_row)
        value = dict(inner_row)
        for join_column in join_columns:
            value.pop(join_column)
        d.setdefault(key, []).append(value)
        # ('e1', 'f1'): {'W': '3'}
    
    for outer_row in outer_rows:
        key = get_join_column_values(outer_row)
        if key in d:
            for value in d[key]:
                joined_row = dict(value)
                joined_row.update(outer_row)
                yield joined_row

def get_rows(file_path, columns):
    """
    Arguments:
        - columns - ['E', 'F', 'W']
    """
    first = True
    for line in open(file_path, 'r'):
        if first:
            first = False
            continue
        line = line.strip('\n')
        if len(line) == 0:
            continue
        words = line.split('\t')
        words += [''] * (len(columns) - len(words))
        
        row = {}
        for column, word in zip(columns, words):
            row[column] = word
        yield row

def test_aggregate1():
    d = group_by_key(['ID'], [
        {'ID': 'a', 'B': '1'},
        {'ID': 'a', 'B': '2'},
        {'ID': 'b', 'B': '3'},
        {'ID': 'c', 'B': '4'},
        {'ID': 'c', 'B': '4'},
        {'ID': 'c', 'B': '4'},
    ])
    print d
    
    d_aggregated = aggregate(d)
    print d_aggregated
    
    assert d_aggregated == {
        ('a',): {'B': None},
        ('b',): {'B': '3'},
        ('c',): {'B': '4'},
    }
#    assert d_flattened == [
#        ['a', None],
#        ['b', '3'],
#        ['c', '4']
#    ]

def test_aggregate2():
    d = group_by_key(['ID'], [
        {'ID': 'a', 'B': '1'},
        {'ID': 'a', 'B': ''},

        {'ID': 'b', 'B': ''},

        {'ID': 'c', 'B': '4'},
        {'ID': 'c', 'B': '5'},
        {'ID': 'c', 'B': ''},
    ])
    
    d_aggregated = aggregate(d)
    
    assert d_aggregated == {
        ('a',): {'B': '1'},
        ('b',): {'B': ''},
        ('c',): {'B': None},
    }
    

def test_join():
    d = join([
        {'ID': 'a', 'B': '1'},
        {'ID': 'a', 'B': '2'},
        {'ID': 'b', 'B': '3'},
        {'ID': 'c', 'B': '4'},
        {'ID': 'c', 'B': '4'},
        {'ID': 'c', 'B': '4'},
    ], [
        {'ID': 'a', 'A': '5'},
        {'ID': 'a', 'A': '6'},
        {'ID': 'a', 'A': '7'},
        {'ID': 'b', 'A': '8'},
        {'ID': 'b', 'A': '9'},
    ],
    ['ID'])
    
    print list(d)
    

if __name__ == '__main__':
    #test_join(); sys.exit(0)
    
    key_columns = sys.argv[1].split()
    
    file1_path = sys.argv[2]
    columns1 = sys.argv[3].split()
    
    file2_path = sys.argv[4]
    columns2 = sys.argv[5].split()
    
    join_columns = sys.argv[6].split()
    out_columns = sys.argv[7].split()
    
    # get rows from both files and merge them by join columns
    rows1 = get_rows(file1_path, columns1)
    rows2 = get_rows(file2_path, columns2)
    rows = join(rows1, rows2, join_columns)
    
    # greoup by key and aggregate by key columns
    d = aggregate(group_by_key(key_columns, rows))
    
    # transform the result back to rows
    rows = to_rows(d, key_columns)
    
    # print rows to the output file in the desired order (out_columns)
    print_rows(sys.stdout, rows, out_columns)
