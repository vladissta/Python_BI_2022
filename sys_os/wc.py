#!/usr/bin/env python3

import sys
import os
import stat
import argparse
import subprocess

# os.chmod('./wc.py', stat.S_IRWXU)

# def counter(inpt):
#     n_lines = 0
#     n_words = 0
#     n_chars = 0
#
#     for line in inpt:
#         if args.l:
#             n_lines += 1
#         if args.w:
#             n_words += len(line.split())
#         if args.c:
#             n_chars += len(line)
#         if True not in (args.l, args.w, args.c):
#             n_lines += 1
#             n_words += len(line.split())
#             n_chars += len(line)
#
#     return n_lines, n_words, n_chars

#
# def lines_counter(inpt):
#     lines = 0
#     for line in inpt:
#         lines += 1
#
#     return lines
#
#
# def words_counter(inpt):
#     # if os.path.isfile(inpt.name):
#     #     inpt.seek(0)
#     words = 0
#     for line in inpt:
#         words += len(line.split())
#
#     return words
#
#
# def character_counter(inpt):
#     # if os.path.isfile(inpt.name):
#     #     inpt.seek(0)
#     char = 0
#     for line in inpt:
#         char += len(line)
#
#     return char


parser = argparse.ArgumentParser()
parser.add_argument('inp', help='file to process',
                    nargs='*',
                    type=argparse.FileType('r'),
                    default=sys.stdin)
parser.add_argument('-l', help='number of lines', action="store_true")
parser.add_argument('-w', help='number of words', action="store_true")
parser.add_argument('-c', help='number of characters', action="store_true")

args = parser.parse_args()

counters = []

# if args.l:
#     counters.append(lines_counter)
# if args.w:
#     counters.append(words_counter)
# if args.c:
#     counters.append(character_counter)
# if True not in (args.l, args.w, args.c):
#     counters = [lines_counter, words_counter, character_counter]

if args.l:
    counters.append(lambda x: 1)
if args.w:
    counters.append(lambda x: len(x.split()))
if args.c:
    counters.append(lambda x: len(x))
if True not in (args.l, args.w, args.c):
    counters = [lambda x: 1, lambda x: len(x.split()), lambda x: len(x)]

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
        sys.stdout.write('\t' + '\t'.join(list(map(str, stats)), ) + f' {inp.name}\n')

if len(total) > 1:
    total_stats_lst = list(zip(*total))
    total_summary = list(map(sum, total_stats_lst))
    sys.stdout.write('\t' + '\t'.join(list(map(str, total_summary)), ) + ' total\n')

# print(stats)

# for func in counters:
#     sys.stdout.write(str(func(data)) + '\t')
# if inp.name != '<stdin>':
#     sys.stdout.write(inp.name + '\n')

#
# for inp in args.inp:
#     data = inp.readlines()
#     for func in counters:
#         sys.stdout.write(str(func(data)) + '\t')
#     if inp.name != '<stdin>':
#         sys.stdout.write(inp.name + '\n')

# print(args.inp)

# lines, words, chars = counter()

# sys.stdout.write(str(args.inp))

# for inp in args.inp:
#     lines, words, chars = counter(inp)
#     if args.l:
#         sys.stdout.write(str(lines) + '\t')
#     if args.w:
#         sys.stdout.write(str(words) + '\t')
#     if args.c:
#         sys.stdout.write(str(chars) + '\t')
#
#     if True not in (args.l, args.w, args.c):
#         sys.stdout.write('\t'.join([str(lines_counter(inp)),
#                                     str(words_counter(inp)),
#                                     str(character_counter(inp))]))
#     sys.stdout.write('\t' + inp.name + '\n')

# for inp in args.inp:
#     if args.l:
#         sys.stdout.write(str(lines_counter(inp)) + '\t')
#     if args.w:
#         sys.stdout.write(str(words_counter(inp)) + '\t')
#     if args.c:
#         sys.stdout.write(str(character_counter(inp)) + '\t')
#
#     if True not in (args.l, args.w, args.c):
#         sys.stdout.write('\t'.join([str(lines_counter(inp)),
#                                     str(words_counter(inp)),
#                                     str(character_counter(inp))]))
#     sys.stdout.write('\t' + inp.name + '\n')
