#!/usr/bin/env python

import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Displays list of contents of directory (current directory by default).',
                                 usage='ls.py [-a] [path ...]')

parser.add_argument('path', default='.', help='directory to show contents', type=str, nargs='*')
parser.add_argument('-a', help='show all files including hidden', action='store_true')

args = parser.parse_args()

several_output = len(args.path) > 1

for path in args.path:
    if not os.path.isdir(path):
        sys.stderr.write(f'Is not a directory: {path}\n')
        sys.exit(1)

    if args.a:
        sys.stdout.write(f'{path}:\n' * several_output)
        sys.stdout.write('\n'.join([os.curdir, os.pardir] +
                                   sorted(os.listdir(path))) + '\n' +
                         "\n" * several_output)
    else:
        sys.stdout.write(f'{path}:\n' * several_output)
        sys.stdout.write(
            '\n'.join(sorted([file for file in os.listdir(path)
                              if not file.startswith('.')])) + '\n' +
            "\n" * several_output * (path != args.path[-1]))
