#!/usr/bin/env python3

import os
import sys
import argparse
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('path', type=str, help='path to delete', nargs='+')
parser.add_argument('-r', action='store_true')

args = parser.parse_args()

if args.r:
    for path in args.path:
        shutil.rmtree(path)
else:
    for path in args.path:
        os.remove(path)
