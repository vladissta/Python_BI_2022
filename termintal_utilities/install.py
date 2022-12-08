#!/usr/bin/env python3

import sys
import os
import shutil

for n, path in enumerate(os.environ['PATH'].split(':')):
    print(n + 1, path)

choice = input('Choose directory to install scripts (write number). '
               'To run default setting (1) press Enter: ')

files = os.listdir('./scripts')

if choice:
    environment = os.environ['PATH'].split(':')[int(choice) - 1]
    for file in files:
        shutil.copy(os.path.join('./scripts', file), os.path.join(environment, file))

else:
    environment = os.environ['PATH'].split(':')[0]
    for file in files:
        shutil.copy(os.path.join('./scripts', file), os.path.join('/usr/local/bin', file))
