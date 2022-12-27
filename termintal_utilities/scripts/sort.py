#!/usr/bin/env python

import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Sorts lines of text alphabetically (default - stdin)',
                                 usage='sort.py [text ...]')

parser.add_argument('text', type=argparse.FileType('r'),
                    help='text to sort', nargs='*', default=[sys.stdin])

args = parser.parse_args()

lines = []
for text in args.text:
    lines.append(text.readlines())

sorted_lines = sorted(sum(lines, []))
for line in sorted_lines:
    sys.stdout.write(line)
