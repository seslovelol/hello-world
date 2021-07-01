# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Aug.03,2020'

import os
import sys
import linecache

def get_lineno(file_path):
    """
        Get 10th line's lineno from the bottom.
    """
    if os.path.isfile(file_path):
        file_reader = open(file_path, 'rb')
        line_count = 0
        while True:
            buffer = file_reader.read(8192*1024)
            if not buffer:
                break
            line_count += buffer.count(b'\n')
        file_reader.close()
        lineno = 0 if line_count < 10 else line_count - 9
        return lineno
    else:
        print('Error: no such file {}'.format(file_path))
        sys.exit(1)


def search_keywords(file_path, keywords):
    """
        Search keywords from logfile's 10 lines in the bottom.
    """
    initial_lineno = get_lineno(file_path)
    length = len(keywords)
    counter = 0
    for _ in range(length):
        lineno = initial_lineno
        for _ in range(10):
            content = linecache.getline(file_path, lineno)
            if keywords[counter] in content:
                counter += 1
                print(content)
                break
            lineno += 1
    if counter == length:
        print('Find all keywords from {}'.format(file_path))
        sys.exit(1)
    else:
        print('Can not find all keywords from {}'.format(file_path))
        sys.exit(1)


if __name__ == "__main__":
    """
        eg: python search.py /path/to/xxx.log keywords1 keywords2
    """
    log_path = sys.argv[1]
    keywords_list = sys.argv[2:]
    search_keywords(log_path, keywords_list)