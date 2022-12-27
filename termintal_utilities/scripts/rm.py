#!/usr/bin/env python

import os
import sys
import argparse
import shutil

parser = argparse.ArgumentParser(description='Removes files or directories',
                                 usage='rm.py [-r] [path ...]')

parser.add_argument('path', type=str, help='directory/file to delete', nargs='+')
parser.add_argument('-r', action='store_true', help='to delete directory recursively ')

args = parser.parse_args()

if args.r:
    for path in args.path:
        shutil.rmtree(path)
else:
    for path in args.path:
        if os.path.isdir(path):
            sys.stderr.write(f'Is a directory: {path}.\nUse rm -r to remove directories\n')
            sys.exit(1)
        os.remove(path)
