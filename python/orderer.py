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
    

if __name__ == '__main__':
    #test_join(); sys.exit(0)
    
    key_columns = sys.argv[1].split()
    columns = sys.argv[2].split()
    
    file1_path = sys.argv[3]
    file2_path = sys.argv[4]
    
    # get rows from both files and merge them by join columns
    rows2 = list(get_rows(file2_path, columns))
    
    d = group_by_key(key_columns, rows2)
    
    for row in get_rows(file1_path, columns):
        x = (row[key_columns[0]],)
        partial_row = d[x]
        values = [x[0]]
        for column in columns:
            if column not in key_columns:
                values.append(list(partial_row[column])[0])
        print '\t'.join(values)
