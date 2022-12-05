import os
import sys
import argparse
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('path', type=str, help='path to delete')
parser.add_argument('-r', action='store_true')

args = parser.parse_args()

if args.r:
    shutil.rmtree(args.path)
else:
    os.remove(args.path)
