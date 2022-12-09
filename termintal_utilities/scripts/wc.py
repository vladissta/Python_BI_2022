#!/usr/bin/env python3

import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inp', help='file to process',
                    nargs='*',
                    type=argparse.FileType('r'), default=[sys.stdin])
parser.add_argument('-l', help='display number of lines', action="store_true")
parser.add_argument('-w', help='display number of words', action="store_true")
parser.add_argument('-c', help='display number of characters', action="store_true")

args = parser.parse_args()

counters = []

if args.l:
    counters.append(lambda x: 1)
if args.w:
    counters.append(lambda x: len(x.split()))
if args.c:
    counters.append(lambda x: len(x))
if True not in (args.l, args.w, args.c):
    counters = [lambda x: 1, lambda x: len(x.split()), lambda x: len(x.encode('utf-8'))]

total = []

for inp in args.inp:
    stats = [0] * len(counters)
    data = inp.readlines()
    for line in data:
        for n, func in enumerate(counters):
            stats[n] += func(line)
    total.append(stats)
    if inp.name == '<stdin>':
        sys.stdout.write('\t' + '\t'.join(list(map(str, stats))) + '\n')
    else:
        sys.stdout.write('\t' + '\t'.join(list(map(str, stats))) + f' {inp.name}\n')

if len(total) > 1:
    total_stats_lst = list(zip(*total))
    total_summary = list(map(sum, total_stats_lst))
    sys.stdout.write('\t' + '\t'.join(list(map(str, total_summary)), ) + ' total\n')
