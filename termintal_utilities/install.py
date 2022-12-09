#!/usr/bin/env python3

import sys
import os
import shutil

for n, path in enumerate(os.environ['PATH'].split(':')):
    print(n + 1, path)

variants = [i + 1 for i in range(len(os.environ['PATH'].split(':')))]

while True:
    choice = int(input('Choose directory to install scripts (write number): '))
    if choice and (choice in variants):
        break
    else:
        print('Choose correct number!')

files = os.listdir('./scripts')

environment = os.environ['PATH'].split(':')[int(choice) - 1]
for file in files:
    shutil.copy(os.path.join('./scripts', file), os.path.join(environment, file))
