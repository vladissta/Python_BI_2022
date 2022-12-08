#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('file', type=argparse.FileType('r'),
                    help='input to sort', nargs='*', default=[sys.stdin])

args = parser.parse_args()

lines = []
for file in args.file:
    lines.append(file.readlines())

sorted_lines = sorted(sum(lines, []))
for line in sorted_lines:
    sys.stdout.write(line)
